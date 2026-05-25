from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from datetime import date, timedelta
import random

from apps.users.models import Client, Instructor
from apps.gym.models import GymHall, Equipment, HallEquipment
from apps.workouts.models import WorkoutType, Group, GroupInstructor, ScheduledClass
from apps.enrollments.models import GroupEnrollment, IndividualSession
from apps.club_cards.models import ClubCard
from apps.promocodes.models import PromoCode
from apps.content.models import News, Vacancy, FAQ, ContactPerson, CompanyHistory
from apps.reviews.models import Review


class Command(BaseCommand):
    help = "Seed all database tables with test data"

    def handle(self, *args, **options):
        self.stdout.write("=" * 50)
        self.stdout.write("STARTING DATABASE SEEDING")
        self.stdout.write("=" * 50)

        # Очищаем все данные (кроме суперпользователя)
        self.stdout.write("Cleaning existing data...")
        
        User.objects.exclude(is_superuser=True).delete()
        WorkoutType.objects.all().delete()
        PromoCode.objects.all().delete()
        Equipment.objects.all().delete()
        GymHall.objects.all().delete()
        HallEquipment.objects.all().delete()
        Instructor.objects.all().delete()
        Client.objects.all().delete()
        ClubCard.objects.all().delete()
        Group.objects.all().delete()
        GroupInstructor.objects.all().delete()
        GroupEnrollment.objects.all().delete()
        ScheduledClass.objects.all().delete()
        IndividualSession.objects.all().delete()
        News.objects.all().delete()
        Review.objects.all().delete()
        FAQ.objects.all().delete()
        Vacancy.objects.all().delete()
        CompanyHistory.objects.all().delete()
        ContactPerson.objects.all().delete()
        
        self.stdout.write("✅ Data cleared")

        # 1. Суперпользователь
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@forsazh.by',
                'is_superuser': True,
                'is_staff': True
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write("✅ Superuser created: admin / admin123")
        else:
            self.stdout.write("ℹ️ Superuser already exists")

        # 2. Workout Types
        wt1 = WorkoutType.objects.create(name="Силовой Кроссфит", description="Интенсивные нагрузки", price_per_session=30, price_per_cycle=220, category="group")
        wt2 = WorkoutType.objects.create(name="Йога Баланс", description="Гибкость и гармония", price_per_session=25, price_per_cycle=180, category="group")
        wt3 = WorkoutType.objects.create(name="Пилатес Реформ", description="Укрепление осанки", price_per_session=28, price_per_cycle=195, category="group")
        wt4 = WorkoutType.objects.create(name="Кардио Марафон", description="Интервальный бег для выносливости", price_per_session=20, price_per_cycle=150, category="group")
        wt5 = WorkoutType.objects.create(name="Индивидуальная тренировка", description="Персональное ведение", price_per_session=45, price_per_cycle=0, category="individual")
        wt6 = WorkoutType.objects.create(name="Экспресс Фитнес-Кураторство", description="Разбор техники", price_per_session=50, price_per_cycle=0, category="individual")
        self.stdout.write("✅ Workout Types: 6")

        # 3. Promo Codes
        PromoCode.objects.create(code="SUMMER20", discount_percent=20, valid_from=timezone.now(), valid_to=timezone.now()+timedelta(days=90), is_active=True, applicable_to="all")
        PromoCode.objects.create(code="FITGROUP", discount_percent=15, valid_from=timezone.now(), valid_to=timezone.now()+timedelta(days=60), is_active=True, applicable_to="group")
        PromoCode.objects.create(code="INDIVIDUAL50", discount_percent=50, valid_from=timezone.now(), valid_to=timezone.now()+timedelta(days=30), is_active=True, applicable_to="individual")
        self.stdout.write("✅ Promo Codes: 3")

        # 4. Gym Halls & Equipment
        eq1 = Equipment.objects.create(name="Беговая дорожка LifeFitness", type="cardio", last_maintenance_date=date.today()-timedelta(days=30))
        eq2 = Equipment.objects.create(name="Велотренажер TechnoGym", type="cardio", last_maintenance_date=date.today()-timedelta(days=45))
        eq3 = Equipment.objects.create(name="Набор TRX лент", type="functional", last_maintenance_date=date.today()-timedelta(days=15))
        eq4 = Equipment.objects.create(name="Гири чугунные", type="functional", last_maintenance_date=date.today()-timedelta(days=60))
        
        hall1 = GymHall.objects.create(name="Основной зал тренинга", capacity=30)
        hall2 = GymHall.objects.create(name="Малый зал функционального тренинга", capacity=15)
        hall3 = GymHall.objects.create(name="Кардио-зона", capacity=20)
        
        HallEquipment.objects.create(hall=hall1, equipment=eq1, quantity=10)
        HallEquipment.objects.create(hall=hall1, equipment=eq4, quantity=12)
        HallEquipment.objects.create(hall=hall2, equipment=eq3, quantity=15)
        HallEquipment.objects.create(hall=hall3, equipment=eq2, quantity=8)
        self.stdout.write("✅ Gym Halls: 3, Equipment: 4")

        # 5. Instructors
        trainers_data = [
            ("trainer_pavel", "Павел Сидоров", 8, [wt1, wt2]),
            ("trainer_olga", "Ольга Козлова", 5, [wt2, wt3]),
            ("trainer_dmitry", "Дмитрий Новиков", 12, [wt1, wt5]),
            ("trainer_elena", "Елена Смирнова", 6, [wt3, wt4]),
            ("trainer_artur", "Артур Петров", 4, [wt2, wt6]),
        ]
        instructors_list = []
        for username, full_name, exp, specializations in trainers_data:
            user = User.objects.create_user(username=username, email=f"{username}@fitness.by", password="trainer123", first_name=full_name.split()[0], last_name=full_name.split()[1])
            inst = Instructor.objects.create(user=user, experience_years=exp, hire_date=date.today() - timedelta(days=365*2))
            inst.specialization.set(specializations)
            instructors_list.append(inst)
        self.stdout.write("✅ Instructors: 5")

        # 6. Clients
        clients_data = [
            ("alex123", "Александр Петров", "1995-04-12", "+375 (29) 111-22-33", "ул. Ленина, д. 5"),
            ("mary_ka", "Мария Ковалева", "1998-09-18", "+375 (29) 222-33-44", "пр. Независимости, д. 45"),
            ("den_bya", "Денис Кравченко", "1990-01-25", "+375 (29) 333-44-55", "ул. Сурганова, д. 18"),
            ("kate_ma", "Екатерина Морозова", "2000-11-05", "+375 (29) 444-55-66", "ул. Коласа, д. 12"),
            ("serg_fa", "Сергей Федоров", "1988-08-30", "+375 (29) 555-66-77", "ул. Некрасова, д. 22"),
            ("vlad_gyma", "Владислав Тарасов", "1993-02-14", "+375 (29) 666-77-88", "ул. Гинтовта, д. 3"),
            ("anna_sa", "Анна Соколова", "2004-07-22", "+375 (29) 777-88-99", "ул. Матусевича, д. 9"),
            ("maxim_pa", "Максим Попов", "1985-05-15", "+375 (29) 888-99-00", "ул. Притыцкого, д. 34"),
            ("julia_ra", "Юлия Рыбакова", "1992-12-01", "+375 (29) 999-00-11", "ул. Филимонова, д. 14"),
            ("artem_ka", "Артем Кузнецов", "1997-06-25", "+375 (29) 123-45-77", "ул. Есенина, д. 8")
        ]
        clients_list = []
        for username, full_name, dob, phone, addr in clients_data:
            user = User.objects.create_user(username=username, email=f"{username}@mail.ru", password="client123", first_name=full_name.split()[0], last_name=full_name.split()[1])
            cl = Client.objects.create(user=user, date_of_birth=dob, phone=phone, address=addr)
            clients_list.append(cl)
        self.stdout.write("✅ Clients: 10")

        # 7. Club Cards
        for i, client in enumerate(clients_list[:7]):
            card = ClubCard.objects.create(
                card_type="monthly",
                price=60,
                valid_from=date.today(),
                valid_to=date.today() + timedelta(days=30),
                client=client
            )
            client.club_card = card
            client.save()
        self.stdout.write("✅ Club Cards: 7")

        # 8. Groups
        g1 = Group.objects.create(name="Кроссфит Утро", workout_type=wt1)
        g2 = Group.objects.create(name="Йога Релакс Вечер", workout_type=wt2)
        g3 = Group.objects.create(name="Пилатес Pro", workout_type=wt3)
        g4 = Group.objects.create(name="Кардио Марафон", workout_type=wt4)
        g5 = Group.objects.create(name="Кроссфит Эксперт", workout_type=wt1)
        
        GroupInstructor.objects.create(group=g1, instructor=instructors_list[0], role="main")
        GroupInstructor.objects.create(group=g2, instructor=instructors_list[1], role="main")
        GroupInstructor.objects.create(group=g3, instructor=instructors_list[3], role="main")
        GroupInstructor.objects.create(group=g4, instructor=instructors_list[2], role="main")
        GroupInstructor.objects.create(group=g5, instructor=instructors_list[0], role="main")
        
        GroupEnrollment.objects.create(client=clients_list[0], group=g1, paid_amount=220, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[1], group=g1, paid_amount=220, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[2], group=g2, paid_amount=180, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[3], group=g2, paid_amount=180, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[4], group=g3, paid_amount=195, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[5], group=g3, paid_amount=195, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[6], group=g4, paid_amount=150, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[7], group=g4, paid_amount=150, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[8], group=g5, paid_amount=220, payment_status="paid")
        GroupEnrollment.objects.create(client=clients_list[9], group=g5, paid_amount=220, payment_status="paid")
        self.stdout.write("✅ Groups: 5, Enrollments: 10")

        # 9. Scheduled Classes
        base_time = timezone.now() + timedelta(days=2)
        halls = [hall1, hall2, hall3]
        for i in range(20):
            sc_start = base_time + timedelta(hours=i*2)
            sc_end = sc_start + timedelta(hours=1)
            group = g1 if i < 5 else (g2 if i < 10 else (g3 if i < 15 else g4))
            sch = ScheduledClass.objects.create(
                group=group,
                start_time=sc_start,
                end_time=sc_end,
                hall=halls[i % 3]
            )
            sch.instructors.add(instructors_list[i % 5])
        self.stdout.write("✅ Scheduled Classes: 20")

        # 10. Individual Sessions
        for i in range(15):
            session_time = timezone.now() - timedelta(days=random.randint(1, 30)) if i < 8 else (timezone.now() + timedelta(days=random.randint(1, 14)))
            status = "completed" if i < 8 else "scheduled"
            IndividualSession.objects.create(
                client=clients_list[i % 10],
                instructor=instructors_list[i % 5],
                workout_type=wt5 if i % 2 == 0 else wt6,
                datetime=session_time,
                duration_minutes=60,
                price=45 if i % 2 == 0 else 50,
                status=status
            )
        self.stdout.write("✅ Individual Sessions: 15")

        # 11. News (с автоматической генерацией slug)
        news_list = [
            {"title": "Открытие нового тренажерного зала!", "summary": "Новое оборудование и просторные залы.", "full_text": "Мы рады сообщить об открытии нового зала с современными тренажерами."},
            {"title": "Скидки на абонементы до 30%", "summary": "Только в мае действуют скидки на все виды абонементов.", "full_text": "В честь весенних праздников скидка 30% на годовой абонемент."},
            {"title": "Новый тренер в команде", "summary": "Присоединился профессиональный тренер по йоге.", "full_text": "Приглашаем всех на занятия йогой с новым тренером."},
            {"title": "Режим работы в праздники", "summary": "Изменение графика работы клуба.", "full_text": "В праздничные дни клуб работает с 10:00 до 18:00."},
            {"title": "Бесплатные тренировки", "summary": "Акция для новых клиентов.", "full_text": "Первое занятие бесплатно при регистрации."},
        ]
        for i, n in enumerate(news_list):
            slug = slugify(n["title"])
            News.objects.create(
                title=n["title"],
                slug=slug,
                summary=n["summary"],
                full_text=n["full_text"],
                published_date=timezone.now() - timedelta(days=i),
                author=admin
            )
        self.stdout.write("✅ News: 5")

        # 12. Reviews
        for i in range(10):
            Review.objects.create(
                client=clients_list[i % 10],
                rating=random.choice([4, 5, 5, 5]),
                text=f"Отличный клуб! Всё понравилось. Рекомендую! Отзыв #{i+1}"
            )
        self.stdout.write("✅ Reviews: 10")

        # 13. FAQ
        faq_list = [
            {"question": "Как записаться на тренировку?", "answer": "Перейдите в раздел Расписание, выберите занятие и нажмите Записаться."},
            {"question": "Как отменить запись?", "answer": "В личном кабинете в разделе Индивидуальные занятия нажмите Отменить."},
            {"question": "Какие документы нужны для регистрации?", "answer": "Паспорт и медицинская справка (при наличии)."},
            {"question": "Есть ли пробное занятие?", "answer": "Да, первое занятие бесплатно для новых клиентов."},
            {"question": "Как купить абонемент?", "answer": "В личном кабинете в разделе Купить абонемент."},
            {"question": "Можно ли заморозить абонемент?", "answer": "Да, на время отпуска или болезни до 30 дней."},
        ]
        for f in faq_list:
            FAQ.objects.create(question=f["question"], answer=f["answer"])
        self.stdout.write("✅ FAQ: 6")

        # 14. Vacancies
        vacancies_list = [
            {"position": "Инструктор по Пилатесу", "description": "Ведение занятий в малых залах. Опыт работы от 1 года."},
            {"position": "Администратор рецепции", "description": "Встреча клиентов, ведение графиков. Знание английского приветствуется."},
            {"position": "Дежурный тренер", "description": "Контроль залов, помощь клиентам. Наличие сертификата."},
            {"position": "Фитнес-тренер", "description": "Проведение групповых и индивидуальных тренировок."},
            {"position": "Менеджер по продажам", "description": "Продажа абонементов, консультация клиентов."},
        ]
        for v in vacancies_list:
            Vacancy.objects.create(position=v["position"], description=v["description"])
        self.stdout.write("✅ Vacancies: 5")

        # 15. Company History
        history_list = [
            (2020, "Основание малого фитнес-клуба 'ФОРСАЖ'"),
            (2021, "Расширение силового зала до 200 кв.м."),
            (2022, "Запуск онлайн записи и мобильного приложения"),
            (2023, "Превышение планки в 1000 активных клиентов"),
            (2024, "Открытие спа-зоны и сауны"),
            (2025, "Тотальная реновация оборудования"),
        ]
        for year, event in history_list:
            CompanyHistory.objects.create(year=year, event=event)
        self.stdout.write("✅ Company History: 6")

        # 16. Contacts
        ContactPerson.objects.create(full_name="Анна Петрова", role="Старший администратор", phone="+375 (29) 111-22-33", email="anna@forsazh.by")
        ContactPerson.objects.create(full_name="Иван Смирнов", role="Менеджер по работе с клиентами", phone="+375 (29) 444-55-66", email="ivan@forsazh.by")
        ContactPerson.objects.create(full_name="Елена Козлова", role="Фитнес-тренер", phone="+375 (29) 777-88-99", email="elena@forsazh.by")
        self.stdout.write("✅ Contacts: 3")

        # Summary
        self.stdout.write("=" * 50)
        self.stdout.write(self.style.SUCCESS("🎉 DATABASE SEEDING COMPLETED!"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"📊 FINAL STATISTICS:")
        self.stdout.write(f"   👤 Users: {User.objects.count()}")
        self.stdout.write(f"   🏃 Clients: {Client.objects.count()}")
        self.stdout.write(f"   🏋️ Instructors: {Instructor.objects.count()}")
        self.stdout.write(f"   📚 Workout Types: {WorkoutType.objects.count()}")
        self.stdout.write(f"   👥 Groups: {Group.objects.count()}")
        self.stdout.write(f"   📅 Scheduled Classes: {ScheduledClass.objects.count()}")
        self.stdout.write(f"   📝 News: {News.objects.count()}")
        self.stdout.write(f"   💼 Vacancies: {Vacancy.objects.count()}")
        self.stdout.write(f"   ❓ FAQ: {FAQ.objects.count()}")
        self.stdout.write(f"   ⭐ Reviews: {Review.objects.count()}")
        self.stdout.write(f"   📞 Contacts: {ContactPerson.objects.count()}")
        self.stdout.write(f"   📖 History: {CompanyHistory.objects.count()}")
        self.stdout.write("=" * 50)
