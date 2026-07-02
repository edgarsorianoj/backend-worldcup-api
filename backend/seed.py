from sqlmodel import Session, select

from src.selections.infraestructure.repositories import (
    engine,
    SelectionModel,
)


selections = [
    {
        "country": "Spain",
        "confederation": "UEFA",
        "captain": "Rodri",
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
    {
        "country": "USA",
        "confederation": "CONCACAF",
        "captain": "Christian Pulisic",
        "coach": "Mauricio Pochettino",
        "world_cups": 0,
        "flag": "https://flagcdn.com/us.svg",
    },
    {
        "country": "Mexico",
        "confederation": "CONCACAF",
        "captain": "Edson Alvarez",
        "coach": "Javier Aguirre",
        "world_cups": 0,
        "flag": "https://flagcdn.com/mx.svg",
    },
    {
        "country": "Canada",
        "confederation": "CONCACAF",
        "captain": "Alphonso Davies",
        "coach": "Jesse Marsch",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ca.svg",
    },
    {
        "country": "England",
        "confederation": "UEFA",
        "captain": "Harry Kane",
        "coach": "Thomas Tuchel",
        "world_cups": 1,
        "flag": "https://flagcdn.com/gb.svg",
    },
    {
        "country": "Croatia",
        "confederation": "UEFA",
        "captain": "Luka Modric",
        "coach": "Zlatko Dalic",
        "world_cups": 0,
        "flag": "https://flagcdn.com/hr.svg",
    },
    {
        "country": "Norway",
        "confederation": "UEFA",
        "captain": "Martin Odegaard",
        "coach": "Stale Solbakken",
        "world_cups": 0,
        "flag": "https://flagcdn.com/no.svg",
    },
    {
        "country": "Netherlands",
        "confederation": "UEFA",
        "captain": "Virgil van Dijk",
        "coach": "Ronald Koeman",
        "world_cups": 0,
        "flag": "https://flagcdn.com/nl.svg",
    },
    {
        "country": "Switzerland",
        "confederation": "UEFA",
        "captain": "Granit Xhaka",
        "coach": "Murat Yakin",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ch.svg",
    },
    {
        "country": "Scotland",
        "confederation": "UEFA",
        "captain": "Andy Robertson",
        "coach": "Steve Clarke",
        "world_cups": 0,
        "flag": "https://flagcdn.com/gb-sct.svg",
    },
    {
        "country": "Austria",
        "confederation": "UEFA",
        "captain": "David Alaba",
        "coach": "Ralf Rangnick",
        "world_cups": 0,
        "flag": "https://flagcdn.com/at.svg",
    },
    {
        "country": "Belgium",
        "confederation": "UEFA",
        "captain": "Kevin De Bruyne",
        "coach": "Domenico Tedesco",
        "world_cups": 0,
        "flag": "https://flagcdn.com/be.svg",
    },
    {
        "country": "Bosnia and Herzegovina",
        "confederation": "UEFA",
        "captain": "Edin Dzeko",
        "coach": "Sergej Barbarez",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ba.svg",
    },
    {
        "country": "Sweden",
        "confederation": "UEFA",
        "captain": "Victor Lindelof",
        "coach": "Jon Dahl Tomasson",
        "world_cups": 0,
        "flag": "https://flagcdn.com/se.svg",
    },
    {
        "country": "Turkiye",
        "confederation": "UEFA",
        "captain": "Hakan Calhanoglu",
        "coach": "Vincenzo Montella",
        "world_cups": 0,
        "flag": "https://flagcdn.com/tr.svg",
    },
    {
        "country": "Czechia",
        "confederation": "UEFA",
        "captain": "Tomas Soucek",
        "coach": "Jaroslav Silhavy",
        "world_cups": 0,
        "flag": "https://flagcdn.com/cz.svg",
    },
    {
        "country": "Colombia",
        "confederation": "CONMEBOL",
        "captain": "James Rodriguez",
        "coach": "Nestor Lorenzo",
        "world_cups": 0,
        "flag": "https://flagcdn.com/co.svg",
    },
    {
        "country": "Ecuador",
        "confederation": "CONMEBOL",
        "captain": "Enner Valencia",
        "coach": "Sebastian Beccacece",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ec.svg",
    },
    {
        "country": "Paraguay",
        "confederation": "CONMEBOL",
        "captain": "Gustavo Gomez",
        "coach": "Gustavo Alfaro",
        "world_cups": 0,
        "flag": "https://flagcdn.com/py.svg",
    },
    {
        "country": "Uruguay",
        "confederation": "CONMEBOL",
        "captain": "Federico Valverde",
        "coach": "Marcelo Bielsa",
        "world_cups": 2,
        "flag": "https://flagcdn.com/uy.svg",
    },
    {
        "country": "Australia",
        "confederation": "AFC",
        "captain": "Jackson Irvine",
        "coach": "Tony Popovic",
        "world_cups": 0,
        "flag": "https://flagcdn.com/au.svg",
    },
    {
        "country": "Iran",
        "confederation": "AFC",
        "captain": "Mehdi Taremi",
        "coach": "Amir Ghalenoei",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ir.svg",
    },
    {
        "country": "Japan",
        "confederation": "AFC",
        "captain": "Wataru Endo",
        "coach": "Hajime Moriyasu",
        "world_cups": 0,
        "flag": "https://flagcdn.com/jp.svg",
    },
    {
        "country": "Jordan",
        "confederation": "AFC",
        "captain": "Mousa Al-Tamari",
        "coach": "Hussein Ammouta",
        "world_cups": 0,
        "flag": "https://flagcdn.com/jo.svg",
    },
    {
        "country": "South Korea",
        "confederation": "AFC",
        "captain": "Son Heung-min",
        "coach": "Hong Myung-bo",
        "world_cups": 0,
        "flag": "https://flagcdn.com/kr.svg",
    },
    {
        "country": "Qatar",
        "confederation": "AFC",
        "captain": "Akram Afif",
        "coach": "Julen Lopetegui",
        "world_cups": 0,
        "flag": "https://flagcdn.com/qa.svg",
    },
    {
        "country": "Saudi Arabia",
        "confederation": "AFC",
        "captain": "Salem Al-Dawsari",
        "coach": "Herve Renard",
        "world_cups": 0,
        "flag": "https://flagcdn.com/sa.svg",
    },
    {
        "country": "Uzbekistan",
        "confederation": "AFC",
        "captain": "Eldor Shomurodov",
        "coach": "Srecko Katanec",
        "world_cups": 0,
        "flag": "https://flagcdn.com/uz.svg",
    },
    {
        "country": "Iraq",
        "confederation": "AFC",
        "captain": "Aymen Hussein",
        "coach": "Jesus Casas",
        "world_cups": 0,
        "flag": "https://flagcdn.com/iq.svg",
    },
    {
        "country": "Morocco",
        "confederation": "CAF",
        "captain": "Achraf Hakimi",
        "coach": "Walid Regragui",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ma.svg",
    },
    {
        "country": "Senegal",
        "confederation": "CAF",
        "captain": "Sadio Mane",
        "coach": "Pape Thiaw",
        "world_cups": 0,
        "flag": "https://flagcdn.com/sn.svg",
    },
    {
        "country": "Egypt",
        "confederation": "CAF",
        "captain": "Mohamed Salah",
        "coach": "Hossam Hassan",
        "world_cups": 0,
        "flag": "https://flagcdn.com/eg.svg",
    },
    {
        "country": "Algeria",
        "confederation": "CAF",
        "captain": "Riyad Mahrez",
        "coach": "Vladimir Petkovic",
        "world_cups": 0,
        "flag": "https://flagcdn.com/dz.svg",
    },
    {
        "country": "Cape Verde",
        "confederation": "CAF",
        "captain": "Ryan Mendes",
        "coach": "Pedro Leitao",
        "world_cups": 0,
        "flag": "https://flagcdn.com/cv.svg",
    },
    {
        "country": "Tunisia",
        "confederation": "CAF",
        "captain": "Wahbi Khazri",
        "coach": "Sami Trabelsi",
        "world_cups": 0,
        "flag": "https://flagcdn.com/tn.svg",
    },
    {
        "country": "Ghana",
        "confederation": "CAF",
        "captain": "Andre Ayew",
        "coach": "Otto Addo",
        "world_cups": 0,
        "flag": "https://flagcdn.com/gh.svg",
    },
    {
        "country": "Ivory Coast",
        "confederation": "CAF",
        "captain": "Franck Kessie",
        "coach": "Emerse Fae",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ci.svg",
    },
    {
        "country": "South Africa",
        "confederation": "CAF",
        "captain": "Percy Tau",
        "coach": "Hugo Broos",
        "world_cups": 0,
        "flag": "https://flagcdn.com/za.svg",
    },
    {
        "country": "DR Congo",
        "confederation": "CAF",
        "captain": "Chancel Mbemba",
        "coach": "Mohamed Ouahbi",
        "world_cups": 0,
        "flag": "https://flagcdn.com/cd.svg",
    },
    {
        "country": "Curacao",
        "confederation": "CONCACAF",
        "captain": "Cuco Martina",
        "coach": "Dick Advocaat",
        "world_cups": 0,
        "flag": "https://flagcdn.com/cw.svg",
    },
    {
        "country": "Haiti",
        "confederation": "CONCACAF",
        "captain": "Johny Placide",
        "coach": "Sebastien Migne",
        "world_cups": 0,
        "flag": "https://flagcdn.com/ht.svg",
    },
    {
        "country": "Panama",
        "confederation": "CONCACAF",
        "captain": "Anibal Godoy",
        "coach": "Thomas Christiansen",
        "world_cups": 0,
        "flag": "https://flagcdn.com/pa.svg",
    },
    {
        "country": "New Zealand",
        "confederation": "OFC",
        "captain": "Chris Wood",
        "coach": "Darren Bazeley",
        "world_cups": 0,
        "flag": "https://flagcdn.com/nz.svg",
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