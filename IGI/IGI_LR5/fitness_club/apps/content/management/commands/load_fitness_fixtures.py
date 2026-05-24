from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta, datetime
import decimal

from apps.users.models import Client, Instructor
from apps.gym.models import GymHall, Equipment, HallEquipment
from apps.workouts.models import WorkoutType, Group, GroupInstructor, ScheduledClass


def _enroll(group, client):
    GroupEnrollment.objects.create(
        client=client,
        group=group,
        paid_amount=group.workout_type.price_per_cycle,
        payment_status='paid',
    )


def _assign_instructor(group, instructor, role='main'):
    GroupInstructor.objects.get_or_create(
        group=group,
        instructor=instructor,
        defaults={'role': role},
    )
from apps.enrollments.models import GroupEnrollment, IndividualSession
from apps.club_cards.models import ClubCard
from apps.promocodes.models import PromoCode
from apps.content.models import News, Vacancy, FAQ, ContactPerson, CompanyHistory
from apps.reviews.models import Review

class Command(BaseCommand):
    help = "Populate Django DB with exact fitness club sample datasets."

    def handle(self, *args, **options):
        self.stdout.write("Drafting initial fitness database seed...")

        # Clear existing entries
        User.objects.exclude(is_superuser=True).delete()
        Equipment.objects.all().delete()
        GymHall.objects.all().delete()
        WorkoutType.objects.all().delete()
        PromoCode.objects.all().delete()
        Vacancy.objects.all().delete()
        FAQ.objects.all().delete()
        CompanyHistory.objects.all().delete()

        # 1. Workout Types (6 items)
        wt1 = WorkoutType.objects.create(name="Силовой Кроссфит", description="Интенсивные нагрузки", price_per_session=30, price_per_cycle=220, category="group")
        wt2 = WorkoutType.objects.create(name="Йога Баланс", description="Гибкость и гармония", price_per_session=25, price_per_cycle=180, category="group")
        wt3 = WorkoutType.objects.create(name="Пилатес Реформ", description="Укрепление осанки", price_per_session=28, price_per_cycle=195, category="group")
        wt4 = WorkoutType.objects.create(name="Кардио Марафон", description="Интервальный бег для выносливости", price_per_session=20, price_per_cycle=150, category="group")
        wt5 = WorkoutType.objects.create(name="Индивидуальная тренировка с Мастером", description="Персональное ведение", price_per_session=45, price_per_cycle=0, category="individual")
        wt6 = WorkoutType.objects.create(name="Экспресс Фитнес-Кураторство", description="Разбор индивидуальной техники", price_per_session=50, price_per_cycle=0, category="individual")

        # 2. Promotional Codes (3 active codes)
        pc1 = PromoCode.objects.create(code="SUMMER20", discount_percent=20, valid_from=timezone.now(), valid_to=timezone.now()+timedelta(days=90), is_active=True, applicable_to="all")
        pc2 = PromoCode.objects.create(code="FITGROUP", discount_percent=15, valid_from=timezone.now(), valid_to=timezone.now()+timedelta(days=60), is_active=True, applicable_to="group")
        pc3 = PromoCode.objects.create(code="INDIVIDUAL50", discount_percent=50, valid_from=timezone.now(), valid_to=timezone.now()+timedelta(days=30), is_active=True, applicable_to="individual")

        # 3. Instructors (5 instructors + User creation)
        trainers_data = [
            ("trainer_pavel1", "Павел Сидоров", 8, [wt1, wt2]),
            ("trainer_olga1", "Ольга Козлова", 5, [wt2, wt3]),
            ("trainer_dmitry1", "Дмитрий Новиков", 12, [wt1, wt5]),
            ("trainer_elena1", "Елена Смирнова", 6, [wt3, wt4]),
            ("trainer_artur1", "Артур Петров", 4, [wt2, wt6]),
        ]
        instructors_list = []
        for username, full_name, exp, specializations in trainers_data:
            u_names = full_name.split()
            first = u_names[1] if len(u_names) > 1 else ""
            last = u_names[0]
            usr = User.objects.create_user(username=username, email=f"{username}@fitness.by", password="strength_trainer_pass", first_name=first, last_name=last)
            inst = Instructor.objects.create(user=usr, experience_years=exp, hire_date=date.today() - timedelta(days=365*2))
            inst.specialization.set(specializations)
            instructors_list.append(inst)

        # 4. Clients (10 clients + User creation)
        clients_data = [
            ("alex123a", "Александр Петров", "1995-04-12", "+375 (29) 111-22-33", "ул. Ленина, д. 5"),
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
            u_names = full_name.split()
            first = u_names[0]
            last = u_names[1] if len(u_names) > 1 else ""
            usr = User.objects.create_user(username=username, email=f"{username}@mail.ru", password="strength_client_pass", first_name=first, last_name=last)
            
            # Initial active ClubCard for 7 users
            card = None
            if len(clients_list) < 7:
                card = ClubCard.objects.create(card_type="monthly", price=60, valid_from=date.today(), valid_to=date.today()+timedelta(days=30))
                
            cl = Client.objects.create(user=usr, date_of_birth=dob, phone=phone, address=addr, club_card=card)
            if card:
                card.client = cl
                card.save()
            clients_list.append(cl)

        # 5. Gym Halls & Equipment
        eq1 = Equipment.objects.create(name="Беговая дорожка LifeFitness", type="cardio", last_maintenance_date=date.today()-timedelta(days=30))
        eq2 = Equipment.objects.create(name="Набор TRX лент", type="functional", last_maintenance_date=date.today()-timedelta(days=15))
        
        hall1 = GymHall.objects.create(name="Основной зал тренинга", capacity=30)
        hall2 = GymHall.objects.create(name="Малый зал функционального тренинга", capacity=15)
        
        HallEquipment.objects.create(hall=hall1, equipment=eq1, quantity=10)
        HallEquipment.objects.create(hall=hall2, equipment=eq2, quantity=15)

        # 6. Groups (5 groups)
        g1 = Group.objects.create(name="Кроссфит Утро", workout_type=wt1)
        _assign_instructor(g1, instructors_list[0])
        _enroll(g1, clients_list[0])
        _enroll(g1, clients_list[1])

        g2 = Group.objects.create(name="Йога Релакс Вечер", workout_type=wt2)
        _assign_instructor(g2, instructors_list[1])
        _enroll(g2, clients_list[2])
        _enroll(g2, clients_list[3])

        g3 = Group.objects.create(name="Пилатес Pro", workout_type=wt3)
        _assign_instructor(g3, instructors_list[3])
        _enroll(g3, clients_list[4])
        _enroll(g3, clients_list[5])

        g4 = Group.objects.create(name="Выносливость 360", workout_type=wt4)
        _assign_instructor(g4, instructors_list[2])
        _enroll(g4, clients_list[6])
        _enroll(g4, clients_list[7])

        g5 = Group.objects.create(name="Кроссфит Эксперт", workout_type=wt1)
        _assign_instructor(g5, instructors_list[0])
        _enroll(g5, clients_list[8])
        _enroll(g5, clients_list[9])

        # 7. Scheduled Classes (15 items)
        base_time = timezone.now() + timedelta(days=2)
        for i in range(15):
            sc_start = base_time + timedelta(hours=i*2)
            sc_end = sc_start + timedelta(hours=1)
            sch = ScheduledClass.objects.create(
                group=g1 if i < 5 else (g2 if i < 10 else g3),
                start_time=sc_start,
                end_time=sc_end,
                hall=hall1 if i % 2 == 0 else hall2
            )
            sch.instructors.add(instructors_list[i % 5])

        # 8. Individual Sessions (10 items)
        for i in range(10):
            session_time = timezone.now() - timedelta(days=2) if i < 4 else (timezone.now() + timedelta(days=i))
            stat_v = "completed" if i < 4 else "scheduled"
            IndividualSession.objects.create(
                client=clients_list[i],
                instructor=instructors_list[i % 5],
                workout_type=wt5 if i % 2 == 0 else wt6,
                datetime=session_time,
                duration_minutes=60,
                status=stat_v
            )

        # 9. Public news (5 news)
        for i in range(5):
            u_author = User.objects.create_user(username=f"author_{i}", password="author_pass")
            News.objects.create(
                title=f"Заголовок важной новости №{i+1}",
                summary=f"Это краткое описание содержания статьи {i+1} для клиентов.",
                full_text=f"Это полный подробный текст официальной статьи фитнес-центра Форсаж под порядковым номером {i+1}.",
                published_date=timezone.now() - timedelta(days=i),
                author=u_author
            )

        # 10. Reviews (5 reviews)
        for i in range(5):
            Review.objects.create(
                client=clients_list[i % 10],
                rating=5 if i % 2 == 0 else 4,
                text=f"Превосходное обслуживание и высокопрофессиональные залы под номером {i+1}"
            )

        # 11. FAQ Items (5 FAQ)
        for i in range(5):
            FAQ.objects.create(
                question=f"Популярный вопрос №{i+1} от клиентов клуба",
                answer=f"Логический выверенный ответ №{i+1} от администрации клуба."
            )

        # 12. Vacancies (3 active)
        Vacancy.objects.create(position="Инструктор по Пилатесу / Стретчингу", salary="2000 - 2500 BYN", description="Ведение занятий в малых залах.")
        Vacancy.objects.create(position="Администратор рецепции", salary="1100 - 1300 BYN", description="Встреча клиентов, ведение графиков.")
        Vacancy.objects.create(position="Дежурный тренер", salary="от 1500 BYN", description="Контроль залов.")

        # 13. Company History
        CompanyHistory.objects.create(year=2021, event="Основание малого фитнес-клуба.")
        CompanyHistory.objects.create(year=2022, event="Расширение силового зала.")
        CompanyHistory.objects.create(year=2023, event="Запуск онлайн записи.")
        CompanyHistory.objects.create(year=2024, event="Превышение планки в 1000 клиентов.")
        CompanyHistory.objects.create(year=2025, event="Тотальная реновация оборудования.")

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with all requested initial entities! Try logging in as admin."))
