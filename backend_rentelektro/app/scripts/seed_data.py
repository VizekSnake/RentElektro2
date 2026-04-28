from __future__ import annotations

from datetime import datetime
from typing import Final, TypedDict

from sqlalchemy.orm import Session

from app.core.database import Base, SessionLocal, engine
from app.modules.rentals.models import AcceptedEnum, Rental
from app.modules.reviews.models import Review
from app.modules.tools.models import Category, Tool
from app.modules.users.models import User


class UserSeed(TypedDict):
    email: str
    username: str
    firstname: str
    lastname: str
    phone: str
    company: bool
    role: str
    is_active: bool
    hashed_password: str
    profile_picture: str


class CategorySeed(TypedDict):
    name: str
    description: str
    active: bool
    creator_username: str


class ToolSeed(TypedDict):
    slug: str
    Type: str
    PowerSource: str
    Brand: str
    Description: str
    category_name: str
    Availability: bool
    Insurance: bool
    Power: int
    Age: float
    RatePerDay: float
    ImageURL: str
    owner_username: str


class RentalSeed(TypedDict):
    tool_slug: str
    renter_username: str
    start_date: datetime
    end_date: datetime
    comment: str
    owner_comment: str
    status: AcceptedEnum
    is_paid: bool
    paid_at: datetime | None
    handed_over_at: datetime | None
    returned_at: datetime | None
    renter_seen_at: datetime | None


class ReviewSeed(TypedDict):
    tool_slug: str
    author_username: str
    rating: float
    comment: str


USER_SEEDS: Final[list[UserSeed]] = [
    {
        "email": "admin@rentelektro.local",
        "username": "admin",
        "firstname": "Admin",
        "lastname": "RentElektro",
        "phone": "500100200",
        "company": True,
        "role": "admin",
        "is_active": True,
        "hashed_password": "$2b$12$ATtVk9tjNUURqhQduDqgUu5Fow8H4p3yWXhiPbbKhX/bm2Md6v.7.",
        "profile_picture": "https://images.unsplash.com/photo-1560250097-0b93528c311a",
    },
    {
        "email": "anna@rentelektro.local",
        "username": "anna_tools",
        "firstname": "Anna",
        "lastname": "Kowalska",
        "phone": "501222333",
        "company": False,
        "role": "user",
        "is_active": True,
        "hashed_password": "$2b$12$G7KNDRE9GwVzB6c7LHc72uOE.hL4SMadIa4387Hd89qLEe6i8ncHe",
        "profile_picture": "https://images.unsplash.com/photo-1494790108377-be9c29b29330",
    },
    {
        "email": "piotr@rentelektro.local",
        "username": "piotr_rent",
        "firstname": "Piotr",
        "lastname": "Nowak",
        "phone": "502333444",
        "company": True,
        "role": "user",
        "is_active": True,
        "hashed_password": "$2b$12$biGCxFZzYRElc4lLtPw3kOcurX2PuUJeeneIU2xK2ALZg52qLjqKS",
        "profile_picture": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e",
    },
    {
        "email": "marta@rentelektro.local",
        "username": "marta_buduje",
        "firstname": "Marta",
        "lastname": "Zielinska",
        "phone": "503444555",
        "company": False,
        "role": "user",
        "is_active": True,
        "hashed_password": "$2b$12$l0TqmlLqwkG2A2dMGy5mc.9/tJnXCTwP4LO/H4yf95N6B35bHANXG",
        "profile_picture": "https://images.unsplash.com/photo-1544005313-94ddf0286df2",
    },
    {
        "email": "tomasz@rentelektro.local",
        "username": "tomasz_event",
        "firstname": "Tomasz",
        "lastname": "Wojcik",
        "phone": "504555666",
        "company": True,
        "role": "user",
        "is_active": True,
        "hashed_password": "$2b$12$ENiG.IQQ.dej1ZLo5bJIxu/5rK8PSIvFHcn0e7SdbUDE92w79MMh6",
        "profile_picture": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d",
    },
]

CATEGORY_SEEDS: Final[list[CategorySeed]] = [
    {
        "name": "Wiertarki",
        "description": "Elektronarzedzia do wiercenia w domu i na budowie.",
        "active": True,
        "creator_username": "admin",
    },
    {
        "name": "Pily",
        "description": "Pily i przecinarki do drewna, metalu i prac ogrodowych.",
        "active": True,
        "creator_username": "piotr_rent",
    },
    {
        "name": "Mloty",
        "description": "Mloty udarowe i wyburzeniowe do ciezszych prac.",
        "active": True,
        "creator_username": "admin",
    },
    {
        "name": "Ogrod",
        "description": "Sprzet do ogrodu, drewna i pielegnacji terenu.",
        "active": True,
        "creator_username": "marta_buduje",
    },
    {
        "name": "Czyszczenie i zasilanie",
        "description": "Agregaty, myjki i sprzet pomocniczy na budowe i eventy.",
        "active": True,
        "creator_username": "tomasz_event",
    },
]

TOOL_SEEDS: Final[list[ToolSeed]] = [
    {
        "slug": "bosch-hammer-drill-gsb-13",
        "Type": "drill",
        "PowerSource": "electric",
        "Brand": "Bosch Professional",
        "Description": "Wiertarka udarowa 900W z walizka i zestawem wiertel.",
        "category_name": "Wiertarki",
        "Availability": True,
        "Insurance": True,
        "Power": 900,
        "Age": 1.5,
        "RatePerDay": 55.0,
        "ImageURL": "https://images.unsplash.com/photo-1504148455328-c376907d081c",
        "owner_username": "anna_tools",
    },
    {
        "slug": "makita-circular-saw-5008mg",
        "Type": "saw",
        "PowerSource": "electric",
        "Brand": "Makita",
        "Description": "Pilarka tarczowa do ciecia desek i plyt OSB.",
        "category_name": "Pily",
        "Availability": True,
        "Insurance": False,
        "Power": 1200,
        "Age": 2.0,
        "RatePerDay": 70.0,
        "ImageURL": "https://images.unsplash.com/photo-1517048676732-d65bc937f952",
        "owner_username": "piotr_rent",
    },
    {
        "slug": "dewalt-rotary-hammer-d25144k",
        "Type": "hammer",
        "PowerSource": "electric",
        "Brand": "DeWalt",
        "Description": "Mlot udarowy SDS do kucia i wiercenia w betonie.",
        "category_name": "Mloty",
        "Availability": False,
        "Insurance": True,
        "Power": 1500,
        "Age": 3.0,
        "RatePerDay": 95.0,
        "ImageURL": "https://images.unsplash.com/photo-1581147036324-c1cfe8d49d75",
        "owner_username": "anna_tools",
    },
    {
        "slug": "milwaukee-combi-drill-m18",
        "Type": "drill_driver",
        "PowerSource": "electric",
        "Brand": "Milwaukee",
        "Description": "Akumulatorowa wiertarko-wkretarka z dwoma bateriami i szybka ladowarka.",
        "category_name": "Wiertarki",
        "Availability": True,
        "Insurance": True,
        "Power": 850,
        "Age": 1.0,
        "RatePerDay": 65.0,
        "ImageURL": "https://images.unsplash.com/photo-1609205807107-e8ec2120f6c4",
        "owner_username": "piotr_rent",
    },
    {
        "slug": "bosch-jigsaw-gst-150",
        "Type": "jigsaw",
        "PowerSource": "electric",
        "Brand": "Bosch Professional",
        "Description": "Wyrzynarka do precyzyjnego ciecia drewna i laminatu, z odsysaniem pylu.",
        "category_name": "Pily",
        "Availability": True,
        "Insurance": False,
        "Power": 780,
        "Age": 1.8,
        "RatePerDay": 48.0,
        "ImageURL": "https://images.unsplash.com/photo-1530124566582-a618bc2615dc",
        "owner_username": "anna_tools",
    },
    {
        "slug": "hilti-demolition-hammer-te-1000",
        "Type": "rotary_hammer",
        "PowerSource": "electric",
        "Brand": "Hilti",
        "Description": "Mlot wyburzeniowy do ciezkich prac remontowych i kucia posadzek.",
        "category_name": "Mloty",
        "Availability": True,
        "Insurance": True,
        "Power": 1700,
        "Age": 2.7,
        "RatePerDay": 140.0,
        "ImageURL": "https://images.unsplash.com/photo-1617575521317-d2974f3b56d2",
        "owner_username": "admin",
    },
    {
        "slug": "karcher-pressure-washer-k7",
        "Type": "pressure_washer",
        "PowerSource": "electric",
        "Brand": "Karcher",
        "Description": "Myjka cisnieniowa do elewacji, kostki brukowej i samochodow.",
        "category_name": "Czyszczenie i zasilanie",
        "Availability": True,
        "Insurance": False,
        "Power": 1800,
        "Age": 1.4,
        "RatePerDay": 85.0,
        "ImageURL": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4",
        "owner_username": "anna_tools",
    },
    {
        "slug": "stihl-chainsaw-ms-182",
        "Type": "chainsaw",
        "PowerSource": "gas",
        "Brand": "Stihl",
        "Description": "Pilarka lancuchowa do prac ogrodowych i przygotowania drewna.",
        "category_name": "Ogrod",
        "Availability": True,
        "Insurance": True,
        "Power": 1600,
        "Age": 2.2,
        "RatePerDay": 92.0,
        "ImageURL": "https://images.unsplash.com/photo-1592928302636-c83cf1e1b7e3",
        "owner_username": "piotr_rent",
    },
    {
        "slug": "honda-generator-eu22i",
        "Type": "generator",
        "PowerSource": "gas",
        "Brand": "Honda",
        "Description": "Cichy agregat pradotworczy na eventy, ogrody i prace bez dostepu do sieci.",
        "category_name": "Czyszczenie i zasilanie",
        "Availability": True,
        "Insurance": True,
        "Power": 2200,
        "Age": 2.5,
        "RatePerDay": 120.0,
        "ImageURL": "https://images.unsplash.com/photo-1581092160607-ee22621dd758",
        "owner_username": "admin",
    },
    {
        "slug": "husqvarna-trimmer-325il",
        "Type": "trimmer",
        "PowerSource": "electric",
        "Brand": "Husqvarna",
        "Description": "Lekka podkaszarka do wykonczenia trawnika przy kraweznikach i ogrodzeniu.",
        "category_name": "Ogrod",
        "Availability": True,
        "Insurance": False,
        "Power": 700,
        "Age": 1.1,
        "RatePerDay": 45.0,
        "ImageURL": "https://images.unsplash.com/photo-1621145239174-3dcdb5d44712",
        "owner_username": "anna_tools",
    },
    {
        "slug": "metabo-angle-grinder-wev-15",
        "Type": "grinder",
        "PowerSource": "electric",
        "Brand": "Metabo",
        "Description": "Szlifierka katowa do metalu, kostki i lekkich prac budowlanych.",
        "category_name": "Mloty",
        "Availability": True,
        "Insurance": False,
        "Power": 1550,
        "Age": 1.9,
        "RatePerDay": 52.0,
        "ImageURL": "https://images.unsplash.com/photo-1504917595217-d4dc5ebe6122",
        "owner_username": "piotr_rent",
    },
    {
        "slug": "einhell-wet-dry-vacuum-te-vc-2230",
        "Type": "industrial_vacuum",
        "PowerSource": "electric",
        "Brand": "Einhell",
        "Description": "Odkurzacz warsztatowy do pylu, gruzu i sprzatania po remoncie.",
        "category_name": "Czyszczenie i zasilanie",
        "Availability": True,
        "Insurance": False,
        "Power": 1150,
        "Age": 1.7,
        "RatePerDay": 42.0,
        "ImageURL": "https://images.unsplash.com/photo-1521207418485-99c705420785",
        "owner_username": "tomasz_event",
    },
    {
        "slug": "ryobi-lawn-mower-rlm18x40h240",
        "Type": "mower",
        "PowerSource": "electric",
        "Brand": "Ryobi",
        "Description": "Akumulatorowa kosiarka do mniejszych ogrodow i trawnikow przy domu.",
        "category_name": "Ogrod",
        "Availability": True,
        "Insurance": False,
        "Power": 1300,
        "Age": 1.3,
        "RatePerDay": 58.0,
        "ImageURL": "https://images.unsplash.com/photo-1621955964441-c173e01c135b",
        "owner_username": "marta_buduje",
    },
    {
        "slug": "dedra-inverter-welder-desi199bt",
        "Type": "welder",
        "PowerSource": "electric",
        "Brand": "Dedra",
        "Description": "Kompaktowa spawarka inwertorowa do lekkich prac warsztatowych i napraw.",
        "category_name": "Mloty",
        "Availability": True,
        "Insurance": True,
        "Power": 200,
        "Age": 2.4,
        "RatePerDay": 76.0,
        "ImageURL": "https://images.unsplash.com/photo-1565439519719-97c9e89f1c47",
        "owner_username": "admin",
    },
    {
        "slug": "yato-compressor-yt-23301",
        "Type": "compressor",
        "PowerSource": "electric",
        "Brand": "Yato",
        "Description": "Kompresor do przedmuchiwania, pompowania i podstawowych narzedzi pneumatycznych.",
        "category_name": "Czyszczenie i zasilanie",
        "Availability": True,
        "Insurance": False,
        "Power": 1500,
        "Age": 1.6,
        "RatePerDay": 50.0,
        "ImageURL": "https://images.unsplash.com/photo-1581092919535-7146ff1a590a",
        "owner_username": "tomasz_event",
    },
]

RENTAL_SEEDS: Final[list[RentalSeed]] = [
    {
        "tool_slug": "makita-circular-saw-5008mg",
        "renter_username": "marta_buduje",
        "start_date": datetime(2026, 4, 1, 8, 0, 0),
        "end_date": datetime(2026, 4, 3, 18, 0, 0),
        "comment": "Potrzebna do docinania blatow i listew podczas wykonczenia kuchni.",
        "owner_comment": "",
        "status": AcceptedEnum.not_viewed,
        "is_paid": False,
        "paid_at": None,
        "handed_over_at": None,
        "returned_at": None,
        "renter_seen_at": None,
    },
    {
        "tool_slug": "milwaukee-combi-drill-m18",
        "renter_username": "anna_tools",
        "start_date": datetime(2026, 4, 4, 9, 0, 0),
        "end_date": datetime(2026, 4, 6, 18, 0, 0),
        "comment": "Szybki wynajem do montazu zabudowy i skrecania konstrukcji stalowej.",
        "owner_comment": "Prosze odebrac po 9:00, zestaw bitow jest w walizce.",
        "status": AcceptedEnum.viewed,
        "is_paid": False,
        "paid_at": None,
        "handed_over_at": None,
        "returned_at": None,
        "renter_seen_at": None,
    },
    {
        "tool_slug": "bosch-hammer-drill-gsb-13",
        "renter_username": "piotr_rent",
        "start_date": datetime(2026, 4, 2, 9, 0, 0),
        "end_date": datetime(2026, 4, 5, 18, 0, 0),
        "comment": "Potrzebuje do montazu konstrukcji pod taras.",
        "owner_comment": "Sprzet przygotowany i sprawdzony przed odbiorem.",
        "status": AcceptedEnum.accepted,
        "is_paid": False,
        "paid_at": None,
        "handed_over_at": None,
        "returned_at": None,
        "renter_seen_at": None,
    },
    {
        "tool_slug": "karcher-pressure-washer-k7",
        "renter_username": "tomasz_event",
        "start_date": datetime(2026, 4, 6, 7, 30, 0),
        "end_date": datetime(2026, 4, 7, 20, 0, 0),
        "comment": "Mycie sceny i barierek po imprezie plenerowej.",
        "owner_comment": "Opłacone, odbior przy magazynie od strony rampy.",
        "status": AcceptedEnum.paid_not_rented,
        "is_paid": True,
        "paid_at": datetime(2026, 4, 5, 16, 15, 0),
        "handed_over_at": None,
        "returned_at": None,
        "renter_seen_at": None,
    },
    {
        "tool_slug": "stihl-chainsaw-ms-182",
        "renter_username": "marta_buduje",
        "start_date": datetime(2026, 4, 8, 8, 0, 0),
        "end_date": datetime(2026, 4, 9, 18, 0, 0),
        "comment": "Potrzebna do porzadkow po wycince na dzialce.",
        "owner_comment": "Lancuch naostrzony, paliwo dolane, prosze nie pracowac bez oslon.",
        "status": AcceptedEnum.paid_rented,
        "is_paid": True,
        "paid_at": datetime(2026, 4, 7, 12, 0, 0),
        "handed_over_at": datetime(2026, 4, 8, 8, 10, 0),
        "returned_at": None,
        "renter_seen_at": None,
    },
    {
        "tool_slug": "dewalt-rotary-hammer-d25144k",
        "renter_username": "admin",
        "start_date": datetime(2026, 4, 10, 8, 0, 0),
        "end_date": datetime(2026, 4, 12, 17, 0, 0),
        "comment": "Krotki wynajem do skucia starej wylewki.",
        "owner_comment": "Po zwrocie sprawdzic przewod zasilajacy.",
        "status": AcceptedEnum.fulfilled,
        "is_paid": True,
        "paid_at": datetime(2026, 4, 8, 10, 30, 0),
        "handed_over_at": datetime(2026, 4, 10, 8, 0, 0),
        "returned_at": datetime(2026, 4, 12, 17, 0, 0),
        "renter_seen_at": datetime(2026, 4, 12, 18, 0, 0),
    },
    {
        "tool_slug": "honda-generator-eu22i",
        "renter_username": "piotr_rent",
        "start_date": datetime(2026, 4, 14, 7, 0, 0),
        "end_date": datetime(2026, 4, 15, 23, 0, 0),
        "comment": "Agregat potrzebny na wydarzenie pod namiotem poza miastem.",
        "owner_comment": "Termin koliduje z innym zleceniem, nie potwierdzam tej rezerwacji.",
        "status": AcceptedEnum.rejected_by_owner,
        "is_paid": False,
        "paid_at": None,
        "handed_over_at": None,
        "returned_at": None,
        "renter_seen_at": datetime(2026, 4, 11, 9, 10, 0),
    },
    {
        "tool_slug": "einhell-wet-dry-vacuum-te-vc-2230",
        "renter_username": "admin",
        "start_date": datetime(2026, 4, 16, 9, 0, 0),
        "end_date": datetime(2026, 4, 17, 17, 0, 0),
        "comment": "Sprzatanie po montazu ekspozycji na targi.",
        "owner_comment": "Mozna odebrac w dniu wynajmu, parking dla busa jest przy hali.",
        "status": AcceptedEnum.accepted,
        "is_paid": False,
        "paid_at": None,
        "handed_over_at": None,
        "returned_at": None,
        "renter_seen_at": None,
    },
    {
        "tool_slug": "ryobi-lawn-mower-rlm18x40h240",
        "renter_username": "tomasz_event",
        "start_date": datetime(2026, 4, 18, 10, 0, 0),
        "end_date": datetime(2026, 4, 19, 16, 0, 0),
        "comment": "Koszenie terenu pod event firmowy i porzadkowanie zieleni.",
        "owner_comment": "W zestawie dwa akumulatory i kosz na trawę.",
        "status": AcceptedEnum.fulfilled,
        "is_paid": True,
        "paid_at": datetime(2026, 4, 17, 19, 0, 0),
        "handed_over_at": datetime(2026, 4, 18, 10, 5, 0),
        "returned_at": datetime(2026, 4, 19, 15, 40, 0),
        "renter_seen_at": datetime(2026, 4, 19, 16, 30, 0),
    },
]

REVIEW_SEEDS: Final[list[ReviewSeed]] = [
    {
        "tool_slug": "bosch-hammer-drill-gsb-13",
        "author_username": "piotr_rent",
        "rating": 4.5,
        "comment": "Sprzet czysty, mocny i gotowy do pracy od razu.",
    },
    {
        "tool_slug": "makita-circular-saw-5008mg",
        "author_username": "admin",
        "rating": 5.0,
        "comment": "Pilarka dobrze utrzymana, ciecie bez problemow.",
    },
    {
        "tool_slug": "stihl-chainsaw-ms-182",
        "author_username": "marta_buduje",
        "rating": 4.8,
        "comment": "Bardzo dobrze przygotowana pilarka, lancuch ostry i sprzet gotowy od razu.",
    },
    {
        "tool_slug": "karcher-pressure-washer-k7",
        "author_username": "tomasz_event",
        "rating": 5.0,
        "comment": "Myjka zrobila robote po wydarzeniu, duze cisnienie i wygodny odbior.",
    },
    {
        "tool_slug": "ryobi-lawn-mower-rlm18x40h240",
        "author_username": "tomasz_event",
        "rating": 4.7,
        "comment": "Lekka i cicha, idealna na krotki wynajem do uporzadkowania terenu przed eventem.",
    },
    {
        "tool_slug": "einhell-wet-dry-vacuum-te-vc-2230",
        "author_username": "admin",
        "rating": 4.4,
        "comment": "Dobry sprzet do szybkiego sprzatania po montazu, nie zapycha sie przy pyle.",
    },
]


def ensure_users(session: Session) -> dict[str, User]:
    users: dict[str, User] = {}
    for item in USER_SEEDS:
        user = session.query(User).filter(User.email == item["email"]).first()
        if user is None:
            user = User(
                email=item["email"],
                username=item["username"],
                firstname=item["firstname"],
                lastname=item["lastname"],
                phone=item["phone"],
                company=item["company"],
                role=item["role"],
                is_active=item["is_active"],
                profile_picture=item["profile_picture"],
                hashed_password=item["hashed_password"],
            )
            session.add(user)
            session.flush()
        users[item["username"]] = user
    return users


def ensure_categories(session: Session, users: dict[str, User]) -> dict[str, Category]:
    categories: dict[str, Category] = {}
    for item in CATEGORY_SEEDS:
        category = session.query(Category).filter(Category.name == item["name"]).first()
        if category is None:
            category = Category(
                name=item["name"],
                description=item["description"],
                active=item["active"],
                creator_id=users[item["creator_username"]].id,
            )
            session.add(category)
            session.flush()
        categories[item["name"]] = category
    return categories


def ensure_tools(
    session: Session, users: dict[str, User], categories: dict[str, Category]
) -> dict[str, Tool]:
    tools: dict[str, Tool] = {}
    for item in TOOL_SEEDS:
        owner = users[item["owner_username"]]
        tool = (
            session.query(Tool)
            .filter(Tool.Brand == item["Brand"], Tool.owner_id == owner.id)
            .first()
        )
        if tool is None:
            tool = Tool(
                Type=item["Type"],
                PowerSource=item["PowerSource"],
                Brand=item["Brand"],
                Description=item["Description"],
                category_id=categories[item["category_name"]].id,
                Availability=item["Availability"],
                Insurance=item["Insurance"],
                Power=item["Power"],
                Age=item["Age"],
                RatePerDay=item["RatePerDay"],
                ImageURL=item["ImageURL"],
                owner_id=owner.id,
            )
            session.add(tool)
            session.flush()
        tools[item["slug"]] = tool
    return tools


def ensure_rentals(session: Session, users: dict[str, User], tools: dict[str, Tool]) -> None:
    for item in RENTAL_SEEDS:
        rental = (
            session.query(Rental)
            .filter(
                Rental.tool_id == tools[item["tool_slug"]].id,
                Rental.user_id == users[item["renter_username"]].id,
                Rental.start_date == item["start_date"],
                Rental.end_date == item["end_date"],
            )
            .first()
        )
        if rental is None:
            rental = Rental(
                tool_id=tools[item["tool_slug"]].id,
                user_id=users[item["renter_username"]].id,
                start_date=item["start_date"],
                end_date=item["end_date"],
                comment=item["comment"],
                owner_comment=item["owner_comment"],
                status=item["status"],
                is_paid=item["is_paid"],
                paid_at=item["paid_at"],
                handed_over_at=item["handed_over_at"],
                returned_at=item["returned_at"],
                renter_seen_at=item["renter_seen_at"],
            )
            session.add(rental)


def ensure_reviews(session: Session, users: dict[str, User], tools: dict[str, Tool]) -> None:
    for item in REVIEW_SEEDS:
        review = (
            session.query(Review)
            .filter(
                Review.tool_id == tools[item["tool_slug"]].id,
                Review.user_id == users[item["author_username"]].id,
            )
            .first()
        )
        if review is None:
            review = Review(
                tool_id=tools[item["tool_slug"]].id,
                user_id=users[item["author_username"]].id,
                rating=item["rating"],
                comment=item["comment"],
            )
            session.add(review)


def seed() -> None:
    session: Session = SessionLocal()
    try:
        Base.metadata.create_all(bind=engine)

        users = ensure_users(session)
        categories = ensure_categories(session, users)
        tools = ensure_tools(session, users, categories)
        ensure_rentals(session, users, tools)
        ensure_reviews(session, users, tools)
        session.commit()

        print("Seed completed.")
        print("Users:")
        print("  admin / admin123")
        print("  anna_tools / anna123")
        print("  piotr_rent / piotr123")
        print("  marta_buduje / marta123")
        print("  tomasz_event / tomasz123")
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
