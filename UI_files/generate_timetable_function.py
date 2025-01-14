from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import ParagraphStyle
from UI_files.connection import create_connection
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import random

def generate_lecture_slots(start_time, end_time, duration_minutes):
    slots = []
    current_time = datetime.strptime(start_time, "%H:%M")
    end_time = datetime.strptime(end_time, "%H:%M")
    duration = timedelta(minutes=duration_minutes)

    while current_time + duration <= end_time:
        slot = f"{current_time.strftime('%H:%M')} - {(current_time + duration).strftime('%H:%M')}"
        slots.append(slot)
        current_time += duration  # Move to next slot

    return slots





def transform_query_to_dictonary(querydata):
    subject_teacher_room = {}

    for _, subject_name, teacher_name, division, prac_batch, room_no in querydata:

        batch = prac_batch if prac_batch else division

        # Simplify the subject name (extract abbreviation if present, else lowercase)
        subject_key = subject_name.lower().split('(')[-1].replace(')',
                                                                  '').strip() if '(' in subject_name else subject_name.lower()

        # Simplify teacher name (use first name, lowercase)
        teacher_key = teacher_name.lower().split()[0]

        # Convert room number to zero-padded string
        room_no_str = str(room_no).zfill(3)

        # Map the (subject, batch) to (teacher, room number)
        subject_teacher_room[(subject_key, batch)] = (teacher_key, room_no_str)
    return subject_teacher_room




conn=create_connection()
def generate_timeTable_func():

    cur=conn.cursor()
    cur.execute("SELECT teacher_name FROM teachers WHERE course_id=3;")
    teachers=[item[0] for item in cur.fetchall()]
    cur.execute("""SELECT st.subToTeacherId, s.subject_name, t.teacher_name, st.division, st.prac_batch, r.room_no FROM subjecttoteacher st JOIN subjects s ON st.subject_id = s.subject_id JOIN teachers t ON st.teacher_id = t.teacher_id JOIN rooms r ON st.room_id = r.room_id WHERE st.batch_id=3;""")
    subject_teacher_room_query=cur.fetchall()
    subject_teacher_room=transform_query_to_dictonary(subject_teacher_room_query)
    # for row in subject_teacher_room:
    #     print(row)
    cur.execute("""SELECT subject_id,subject_name,semester FROM subjects WHERE course_id=3""")
    subjects=[item[1] for item in cur.fetchall()]
    cur.execute("""SELECT DISTINCT room_no FROM rooms""")
    rooms_query=[item[0] for item in cur.fetchall()]
    rooms=[str(num).zfill(3) for num in rooms_query]
    # # divisions
    cur.execute("SELECT DISTINCT division FROM subjecttoteacher WHERE division IS NOT NULL AND division <> '';")
    batches=[row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT prac_batch FROM subjecttoteacher WHERE prac_batch IS NOT NULL AND prac_batch <> '';")
    sub_batches=[row[0] for row in cur.fetchall()]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    #
    time_slots = ['9-10', '10-11', '11-1', '1-3']
    #
    # # timeSlots_for_prac=generate_lecture_slots("2:00","4:00",120)
    # print(teachers)
    # for row in subject_teacher_room:
    #     print(row)
    # print(subject_teacher_room)
    # print(batches)
    # print(sub_batches)
    # print(subjects)
    # print(rooms)


    #Gene: (Subject, Teacher, Room, Day, Time Slot, Batch)
    def create_gene(subject, division, duration=1):
        teacher, room = subject_teacher_room[(subject, division)]
        day = random.choice(days)
        start_slot = random.choice(time_slots[:len(time_slots) - duration + 1])
        return (subject, teacher, room, day, start_slot, division, duration)

    # Chromosome: a complete timetable (list of genes)
    def create_chromosome():
        chromosome = []

        # For Divisions A and B (2 lectures/day)
        for division in batches:
            subjects_for_division = [subj for (subj, div), _ in subject_teacher_room.items() if div == division]
            for day in days:
                daily_subjects = random.sample(subjects_for_division, 2)  # Ensure exactly 2 lectures per day
                for subject in daily_subjects:
                    chromosome.append(create_gene(subject, division))

        # For Sub-divisions B1, B2, B3, B4 (1 practical of 2 hours/day)
        for sub_batch in sub_batches:
            subjects_for_sub_batch = [subj for (subj, div), _ in subject_teacher_room.items() if div == sub_batch]
            for day in days:
                subject = random.choice(subjects_for_sub_batch)  # Ensure exactly 1 session per day
                chromosome.append(create_gene(subject, sub_batch, duration=2))  # 2-hour practical session

        return chromosome

    # Population: a collection of chromosomes
    def create_population(size):
        return [create_chromosome() for _ in range(size)]

    # Fitness Function: penalize conflicts
    def fitness(chromosome):
        score = 0
        seen = set()
        for gene in chromosome:
            subject, teacher, room, day, start_slot, division, duration = gene
            time_slots_range = time_slots[time_slots.index(start_slot):time_slots.index(start_slot) + duration]
            for slot in time_slots_range:
                key = (teacher, day, slot)
                room_key = (room, day, slot)
                if key in seen or room_key in seen:
                    score -= 10  # Conflict
                else:
                    seen.add(key)
                    seen.add(room_key)
        return score

    # Selection: choose the best chromosomes
    def selection(population):
        return sorted(population, key=fitness, reverse=True)[:2]

    # Crossover: swap parts between parents
    def crossover(parent1, parent2):
        point = random.randint(1, len(parent1) - 2)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2

    # Mutation: randomly change a gene
    def mutate(chromosome, mutation_rate=0.1):
        for i in range(len(chromosome)):
            if random.random() < mutation_rate:
                division = chromosome[i][5]
                duration = chromosome[i][6]
                subject = random.choice([subj for subj, div in subject_teacher_room if div == division])
                chromosome[i] = create_gene(subject, division, duration)
        return chromosome

    # Genetic Algorithm
    def genetic_algorithm(pop_size, generations):
        population = create_population(pop_size)
        for gen in range(generations):
            population = selection(population)
            next_gen = []
            while len(next_gen) < pop_size:
                parent1, parent2 = random.sample(population, 2)
                child1, child2 = crossover(parent1, parent2)
                next_gen.append(mutate(child1))
                next_gen.append(mutate(child2))
            population = next_gen
            best_fit = fitness(selection(population)[0])
            print(f"Generation {gen + 1}, Best Fitness: {best_fit}")
            if best_fit == 0:
                break
        return selection(population)[0]

    # Print Timetable Day-wise and Time-wise
    def print_timetable(timetable):
        timetable_sorted = sorted(timetable, key=lambda x: (days.index(x[3]), time_slots.index(x[4]), x[5]))
        current_day = ""
        for session in timetable_sorted:
            day = session[3]
            if day != current_day:
                current_day = day
                print(f"\n{day}:")
            duration = session[6]
            print(
                f"  {session[4]} ({duration} hr) - {session[0]} (Teacher: {session[1]}, Room: {session[2]}, Division: {session[5]})")

    # Run the algorithm
    best_timetable = genetic_algorithm(pop_size=20, generations=100)
    print("\nBest Timetable:")

    def generate_pdf_timetable(timetable, filename="timetable.pdf"):

        # Sort timetable by day, time, and division
        timetable_sorted = sorted(timetable, key=lambda x: (days.index(x[3]), time_slots.index(x[4]), x[5]))

        # Group sessions by weekday
        days_data = {day: [] for day in days}
        for session in timetable_sorted:
            days_data[session[3]].append(session)

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Add table for each weekday
        for day, sessions in days_data.items():
            elements.append(
                Paragraph(f"<b>{day}</b>", style=ParagraphStyle(name="Heading", fontSize=14, spaceAfter=10)))
            data = [["Time Slot", "Subject", "Teacher", "Room", "Division"]]

            for session in sessions:
                data.append([session[4], session[0], session[1], session[2], session[5]])

            # Create table
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))  # Add spacing after each table

        # Build PDF
        doc.build(elements)
        print(f"PDF generated: {filename}")
    generate_pdf_timetable(best_timetable)
    print_timetable(best_timetable)


# Sample data (IDs for simplicity)
# subjects = ["DSA",'spm','aj','mfcs','ecommerce','aj lab','wt lab','adbms','adbms lab']
# teachers = ['pankaj', 'neha', 'sanju', 'shilpa','anup','snehil','swasthi','roshna mam']
# rooms = ['102', '103', '001','002','003','004']
#
 # 4 lectures per day
# batches = ['A', 'B']
# sub_batches=["B1","B2","B3","B4"]
# # Mapping: (Subject, Division) → (Teacher, Room)
# subject_teacher_room = {
#     ('adbms', 'A'): ('neha', '103'),
#     ('spm', 'A'): ('anup', '103'),
#     ('mfcs', 'A'): ('neha', '103'),
#     ('DSA','B4'):('sanju','004'),
#     ('DSA', 'B3'): ('shilpa', '003'),
#     ('DSA',"B1"):("shilpa",'001'),
#     ('ecommerce','A'):("sanju",'103'),
#     ('ecommerce', 'B'): ('sanju', '102'),
#     ('adbms', 'B'): ('neha', '102'),
#     ('spm', 'B'): ('anup', '102'),
#     ('mfcs', 'B'): ('snehil', '102'),
#     ('aj', 'B'): ('pankaj', '102'),
#     ('adbms lab', 'B2'): ('neha', '004'),
#     ('DSA',"B2"):('shilpa','002'),
#     ('aj lab','B1'):('pankaj','001'),
#     ('aj lab','B2'):('pankaj','003'),
#     ('aj lab','B3'):('pankaj','002'),
#     ('aj lab','B4'):('pankaj','004'),
#     ('wt lab','B1'):('roshna','001'),
#     ('wt lab', 'B2'):('roshna', '002'),
#     ('wt lab','B3'):("roshna",'003'),
#     ('wt lab','B4'):('anup','004'),
#
# }
generate_timeTable_func()
