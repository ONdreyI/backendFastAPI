def data_iterator():
    yield {
        "endpoint": "/auth/register",
        "json_data": {"email": "kot@pes.com", "password": "1234"},
    }
    yield {
        "endpoint": "/hotels",
        "json_data": [
            {
                "title": "Cosmos Collection Altay Resort",
                "location": "Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20",
            },
            {
                "title": "Skala",
                "location": "Республика Алтай, Майминский район, поселок Барангол, Чуйская улица 40а",
            },
            {
                "title": "Bridge Resort",
                "location": "посёлок городского типа Сириус, Фигурная улица, 45",
            },
        ],
    }
    yield {
        "endpoint": "/hotels/{hotel_id}/rooms",
        "json_data": [
            {
                "hotel_id": 1,
                "title": "Улучшенный с террасой и видом на озеро",
                "description": "Невероятный красоты номер.",
                "price": 24500,
                "quantity": 5,
            },
            {
                "hotel_id": 1,
                "title": "Делюкс Плюс",
                "description": "Лучший номер отеля.",
                "price": 22450,
                "quantity": 10,
            },
            {
                "hotel_id": 2,
                "title": "Номер на 2-х человек",
                "description": "Красота неописуемая.",
                "price": 4570,
                "quantity": 15,
            },
            {
                "hotel_id": 3,
                "title": "Номер на 3-х человек",
                "description": None,
                "price": 4350,
                "quantity": 8,
            },
        ],
    }
