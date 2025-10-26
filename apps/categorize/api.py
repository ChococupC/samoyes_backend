from fastapi import APIRouter, Depends
import random
from datetime import timedelta, datetime
from apps.categorize.models import CategorizeDaily, Word, Category
from apps.categorize.schemas import CategorizeInput
from utils.Sqlalchemy.connect import transactional
from utils.fastapi_utils.debug.debug import DebugManager
from utils.pydantic_utils.response import SuccessResponseModel, ErrorResponseModel

router = APIRouter(tags=["categorize"], prefix="/categorize")

@router.get("/")
async def categorize_get(param: CategorizeInput = Depends(),
                         debugger: DebugManager = Depends()):
    """
        Grab words for the day
        :return: date, categories, words, puzzle_words
    """
    debugger.enabled = False

    # Get category for today
    dt = param.date
    if not dt:
        return ErrorResponseModel(message="No date provided")

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
def categorize_create(debugger: DebugManager = Depends()):
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
            [5, 5, 6, 8, 4, 2],     #1
        ]
        month_weight = abs(month - 9)
        result = weights[month_weight]

        if debugger.enabled:
            debugger.add(
                method="GetWeight",
                month = month_weight,
                weight = result
            )

        return result

    def group_categorize(categories):
        """
        Groups 30 categories (each with 4 random words) into 7 groups of 16 words.
        Ensures no duplicate words within each group.
        28 categories are used (7 groups × 4 categories), 2 serve as buffer for deferrals.
        """
        current_group = []
        deferred_categories = []
        groups_return = []
        seen_words_in_group = set()

        for category in categories:
            # Get 4 random words from this category
            word_inst = Word.objects().filter(category=category.id).all()
            randomized_category_words = random.sample(word_inst, 4)

            # Check if any word already exists in current group
            word_names = [word.name for word in randomized_category_words]
            has_duplicate = any(name in seen_words_in_group for name in word_names)

            if has_duplicate:
                # Defer this category for later use
                deferred_categories.append(randomized_category_words)
            else:
                # Add to current group
                current_group.extend(randomized_category_words)
                seen_words_in_group.update(word_names)

                # Check if current group is complete (16 words = 4 categories × 4 words)
                if len(current_group) == 16:
                    groups_return.append(current_group)
                    current_group = []
                    seen_words_in_group = set()

                    # Try to use deferred categories for next group
                    for deferred_words in deferred_categories[:]:
                        deferred_names = [word.name for word in deferred_words]
                        if not any(name in seen_words_in_group for name in deferred_names):
                            current_group.extend(deferred_words)
                            seen_words_in_group.update(deferred_names)
                            deferred_categories.remove(deferred_words)

                            if len(current_group) == 16:
                                groups_return.append(current_group)
                                current_group = []
                                seen_words_in_group = set()
                                break

        # Debug logging
        if debugger.enabled:
            debugger.add(
                method="GroupCategorize",
                status=len(groups_return) == 7,
                groups_return=[[w.name for w in g ] for g in groups_return],
                deferred_count=len(deferred_categories),
                group_sizes=[len(g) for g in groups_return]
            )

        # Validation
        if len(groups_return) != 7:
            if debugger.enabled:
                debugger.display()
            raise ValueError(
                f"Expected 7 groups, got {len(groups_return)}. "
                f"Deferred categories: {len(deferred_categories)}"
            )

        return groups_return

    # 1. Check if code runs at a correct date
    dt = datetime.now().date()

    if not debugger.enabled:
        latest_inst = CategorizeDaily.get_latest_instance(debugger=debugger)
        if latest_inst.date > dt:

            if debugger.enabled:
                debugger.display()

            return ErrorResponseModel(message=f"Operate too early, please wait till {latest_inst.date}")

    # 2. Get weight for each unit
    weight = get_weight(dt.month)

    # 3. Get Random Categories By Unit
    randomized_categories = []

    for i in range(0,6):
        k = weight[i]
        category_inst = Category.get_instances_all(debugger=debugger, unit=i)
        randomized_category = random.sample(category_inst, k)
        randomized_categories.extend(randomized_category)

    random.shuffle(randomized_categories)

    # 4. Form word groups
    groups = group_categorize(randomized_categories)

    # 5. Store words in CategorizeDaily
    if debugger.enabled:
        debugger.add(model=CategorizeDaily, method="categorize_word")
        debugger.display()

        return SuccessResponseModel(message="categorize_word complete")

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

    return SuccessResponseModel(message="categorize_word complete")

