from application.services.faker import faker


# Name_generator__start
def name_generate() -> str:
    name = faker.name().split()[0]
    email = f"{str(name.split()[0]).lower()}_example@mail.com"
    return f"{name}: {email}"
