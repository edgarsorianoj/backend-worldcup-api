from sqlmodel import Session, select

from src.selections.infraestructure.repositories import (
    engine,
    SelectionModel,
)


selections = [
    {
        "country": "Spain",
        "confederation": "UEFA",
        "captain": "Alvaro Morata",
        "coach": "Luis de la Fuente",
        "world_cups": 1,
        "flag": "https://flagcdn.com/es.svg",
    },
    {
        "country": "Argentina",
        "confederation": "CONMEBOL",
        "captain": "Lionel Messi",
        "coach": "Lionel Scaloni",
        "world_cups": 3,
        "flag": "https://flagcdn.com/ar.svg",
    },
    {
        "country": "Brazil",
        "confederation": "CONMEBOL",
        "captain": "Bruno Guimaraes",
        "coach": "Carlo Ancelotti",
        "world_cups": 5,
        "flag": "https://flagcdn.com/br.svg",
    },
    {
        "country": "France",
        "confederation": "UEFA",
        "captain": "Kylian Mbappe",
        "coach": "Didier Deschamps",
        "world_cups": 2,
        "flag": "https://flagcdn.com/fr.svg",
    },
    {
        "country": "Germany",
        "confederation": "UEFA",
        "captain": "Joshua Kimmich",
        "coach": "Julian Nagelsmann",
        "world_cups": 4,
        "flag": "https://flagcdn.com/de.svg",
    },
    {
        "country": "Portugal",
        "confederation": "UEFA",
        "captain": "Cristiano Ronaldo",
        "coach": "Roberto Martinez",
        "world_cups": 0,
        "flag": "https://flagcdn.com/pt.svg",
    },
]


def seed():

    with Session(engine) as session:

        for selection in selections:

            existing = session.exec(
                select(SelectionModel).where(
                    SelectionModel.country == selection["country"]
                )
            ).first()

            if existing:
                print(
                    f"{selection['country']} already exists, skipping"
                )
                continue

            selection_model = SelectionModel(
                country=selection["country"],
                confederation=selection["confederation"],
                captain=selection["captain"],
                coach=selection["coach"],
                world_cups=selection["world_cups"],
                flag=selection["flag"],
            )

            session.add(selection_model)

        session.commit()


if __name__ == "__main__":
    seed()
    print("Database seeded successfully")