import pytest



data = {"name":"omlet", "cook_time":"13", "descript": "for breakfast", "ingredients": "milk, eags", }


@pytest.mark.asyncio
async  def test_recipe_by_id(client):
    """
    Тест проверки эндпоинта для поиска рецепта по его id.Используется фикстура по созданию подключения, а, следовательно
    и создания БД с одной записью.
    Проверяется получение статуса запроса =200, длины ответа (6 ключей), и значения названия рецепта, равного
    переданному ("омлет").
    """
    recipe_id = 1
    response = await client.get(f"/recipes/{recipe_id}")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert response.json()["name"] == "Test omlet"


@pytest.mark.asyncio
async def test_recipes(client, test_recipe):
    """
    Тест для проверки эндроинта, возвращающего список находящихся в базе рецептов. Используется фикстура по созданию
    подключения, содержащая в себе создание БД и добавление в нее записи, а также по добавлению второй записи
    test_recipe.
    Проверяется статус ответа (=200), длина ответа( так как создается две записи -
    одна при создании таблицы, вторая фикстурой test_recipe).
    """
    response = await client.get("/recipes/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    print(response.json())


@pytest.mark.asyncio
async def test_recipess(client):
    """
    Тест для проверки эндроинта, возвращающего список находящихся в базе рецептов. Используется фикстура по созданию
    подключения, содержащая в себе создание БД и добавление в нее записи.
    Проверяется статус ответа (=200), длина ответа == 1 при создании только одной записи функцией setup_db.
    """
    response = await client.get("/recipes/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    print(response.json())
    assert response.json()[0]["name"] == "Test omlet"

@pytest.mark.asyncio
async def test_post(client):
    """
    Тест для проверки эгдпоинта по добавлению нового рецепта. Используется фикстура по созданию
    подключения, содержащая в себе создание БД и добавление в нее записи. Проверяется статус ответа, длтна словарика, и
    значение поля "время приготовления" и "имя"= переданному (13 и омлет)
    """
    response = await client.post("/recipes/", json=data)
    assert response.status_code == 200
    assert len(response.json()) == 6
    assert response.json()["cook_time"] == 13
    assert response.json()["name"] == "omlet"
    print(response.json()["cook_time"])


