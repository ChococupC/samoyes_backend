from fastapi import APIRouter, Depends
import random
from datetime import timedelta, datetime
from apps.categorize.models import CategorizeDaily, Word, Category
from utils.Sqlalchemy.connect import transactional
from utils.fastapi_utils.debug.debug import DebugManager
from utils.pydantic_utils.response import SuccessResponseModel, ErrorResponseModel

router = APIRouter(tags=["categorize"], prefix="/categorize")

@router.get("/")
async def categorize_get(debugger: DebugManager = Depends()):
    """
        Grab words for the day
        :return: date, categories, words, puzzle_words
    """
    debugger.enabled = False

    # Get category for today
    dt = datetime.now().date()
    words = CategorizeDaily.get_instances_all(error=False, debugger=debugger, o="category", date=dt)

    if not words:
        if debugger.enabled:
            debugger.display()
        return ErrorResponseModel(message="No category today due to maintenance, please come again tomorrow!")

    # Create Category List (dict.fromkeys, keep all unique categories)
    categories_get = []
    categories = list(dict.fromkeys([inst.category for inst in words]))
    for c_id in categories:
        category_inst = Category.get_instance_by_pk(debugger=debugger, pk=c_id)
        categories_get.append(category_inst.name)

    # Create Word List (
    words_name = [word.name for word in words]
    words_get = [words_name[i:i+4] for i in range(0,16,4)]

    #Create Puzzle Word List
    puzzle_words_inst = CategorizeDaily.get_instances_all(debugger=debugger, o="position", date=dt)
    puzzle_words_get = [inst.name for inst in puzzle_words_inst]

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel(data={
        "date" : dt,
        "categories" : categories_get,
        "words" : words_get,
        "puzzle_words" : puzzle_words_get,
    })

@router.get("/create/")
async def categorize_word(debugger: DebugManager = Depends()):
    """
    Create new combination of categories for this week.
    1) check if code runs at the correct date
    2) get the weight for each unit
    3) randomly grab categories from each unit (amount determined by weight)
    4) grab the words from each category to form 7 groups of 4
    5) store words in CategorizeDaily
    :return: none
    """
    debugger.enabled = False

    def get_weight(month):
        # Returns the category weight
        weights = [
            [17, 13, 0, 0, 0, 0],   #9
            [11, 15, 4, 0, 0, 0],   #8,10
            [6, 9, 11, 4, 0, 0],    #7,11
            [7, 8, 8, 7, 0, 0],     #6,12
            [4, 5, 6, 6, 5, 4],     #5
            [4, 5, 6, 5, 6, 4],     #4
            [4, 4, 5, 5, 5, 7],     #3
            [5, 5, 4, 5, 8, 3],     #2
            [5, 5, 6, 8, 4, 0],     #1
        ]
        month_weight = abs(month - 9)
        result = weights[month_weight]

        if debugger.enabled:
            debugger.add(
                model="No Model",
                method="GetWeight",
                month = month_weight,
                weight = result
            )

        return result

    def group_categorize(categories):
        words_group = []
        repeated_category_words = []
        groups_return = []

        for category in categories:
            word_inst = Word.objects().filter(category=category.id).all()
            randomized_category_words = random.sample(word_inst, 4)
            words_group.extend(randomized_category_words)
            len_words_group = len(words_group)
            if len_words_group != len(set(words_group)):
                repeated_category_words.extend(randomized_category_words)
                words_group.reverse()

            elif len_words_group == 16:
                groups_return.append(words_group)
                words_group = repeated_category_words
                repeated_category_words = []

        if debugger.enabled:
            debugger.add(
                model="No Model",
                method = "GroupCategorize",
                status = bool(len(groups_return) == 7),
                groups_return = groups_return
            )

        if len(groups_return) != 7:
            if debugger.enabled:
                debugger.display()

            raise ValueError(f"Group Return Only have {len(groups_return)}")
        return groups_return

    # 1. Check if code runs at a correct date
    dt = datetime.now().date()

    latest_inst = CategorizeDaily.get_latest_instance(debugger=debugger)
    if latest_inst.date > dt:

        if debugger.enabled:
            debugger.display()

        return ErrorResponseModel(message=f"Operate too early, please wait till {latest_inst.date}")

    # 2. Get weight for each unit
    weight = get_weight(dt.month)
    randomized_categories = []

    # 3. Get Random Categories By Unit
    for i in range(0,6):
        k = weight[i]
        category_inst = Category.get_instances_all(debugger=debugger, unit=i)
        randomized_category = random.sample(category_inst, k)
        randomized_categories.extend(randomized_category)

    random.shuffle(randomized_categories)

    # 4. Form word groups
    groups = group_categorize(randomized_categories)

    # 5. Store words in CategorizeDaily
    with transactional() as db:
        for group in groups:
            dt += timedelta(days=1)

            position_list = list(range(1, 17))
            random.shuffle(position_list)

            for i, word in enumerate(group):
                CategorizeDaily.add_instance(
                    db=db,
                    debugger=debugger,
                    date=dt,
                    word=word.id,
                    category=word.category,
                    position=position_list[i],
                    name=word.name
                )

    if debugger.enabled:
        debugger.display()

    return SuccessResponseModel(message="categorize_word complete")

