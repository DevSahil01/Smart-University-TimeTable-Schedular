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
def generate_timeTable_func(batchid):

    cur=conn.cursor()
    cur.execute("SELECT course_id FROM batch WHERE batch_id=(%s)",(batchid,))
    courseId=cur.fetchall()[0][0]
    cur.execute("SELECT teacher_name FROM teachers WHERE course_id=(%s)",(courseId,))
    teachers=[item[0] for item in cur.fetchall()]
    cur.execute("""SELECT st.subjectToTeacherID, s.subject_name, t.teacher_name, st.division, st.prac_batch, r.room_no FROM subjecttoteacher st JOIN subjects s ON st.subject_id = s.subject_id JOIN teachers t ON st.teacher_id = t.teacher_id JOIN rooms r ON st.room_id = r.room_id WHERE st.batch_id=(%s);""",
                (batchid,))
    subject_teacher_room_query=cur.fetchall()
    subject_teacher_room=transform_query_to_dictonary(subject_teacher_room_query)
    # for row in subject_teacher_room:
    #     print(row)
    cur.execute("""SELECT subject_id,subject_name,semester FROM subjects WHERE course_id=(%s)""",(courseId,))
    subjects=[item[1] for item in cur.fetchall()]
    cur.execute("""SELECT DISTINCT room_no FROM rooms""")
    rooms_query=[item[0] for item in cur.fetchall()]
    rooms=[str(num).zfill(3) for num in rooms_query]
    # # divisions
    cur.execute("SELECT DISTINCT division FROM subjecttoteacher WHERE division IS NOT NULL AND division <> '';")
    batches=[row[0] for row in cur.fetchall()]
    cur.execute("SELECT DISTINCT prac_batch FROM subjecttoteacher WHERE prac_batch IS NOT NULL AND prac_batch <> '';")
    practical_batches=[row[0] for row in cur.fetchall()]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    #
    time_slots = ['9-10', '10-11', '11-1', '1-3','3-5']
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
    def create_gene(subject, division):
        teacher, room = subject_teacher_room[(subject, division)]
        return (subject, teacher, room, random.choice(days), random.choice(time_slots), division)

    # Chromosome: a complete timetable (list of genes)
    def create_chromosome():
        chromosome = []
        for division in batches:
            subjects_for_division = [subj for subj, div in subject_teacher_room if div == division]
            for day in days:
                daily_subjects = random.choices(subjects_for_division, k=2)  # 2 lectures per day for A/B
                for i, time_slot in enumerate(time_slots[:2]):
                    subject = daily_subjects[i]
                    chromosome.append(create_gene(subject, division)[:3] + (day, time_slot, division))

        # Assign synchronized practicals to practical batches
        practical_subjects = [subj for subj, div in subject_teacher_room if div in practical_batches]
        for day in days:
            practical_time_slot = random.choice(time_slots[2:])  # Assign to later slots
            selected_subjects = random.sample(practical_subjects, 4)
            for i, batch in enumerate(practical_batches):
                subject = selected_subjects[i % len(selected_subjects)]
                chromosome.append(create_gene(subject, batch)[:3] + (day, practical_time_slot, batch))
        return chromosome

    # Population: a collection of chromosomes
    def create_population(size):
        return [create_chromosome() for _ in range(size)]

    # Fitness Function: penalize conflicts
    def fitness(chromosome):
        score = 0
        seen = set()
        for gene in chromosome:
            key = (gene[1], gene[3], gene[4])  # (Teacher, Day, Time Slot)
            room_key = (gene[2], gene[3], gene[4])  # (Room, Day, Time Slot)
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
                subject = random.choice([subj for subj, div in subject_teacher_room if div == division])
                chromosome[i] = create_gene(subject, division)
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
            print(f"  {session[4]} - {session[0]} (Teacher: {session[1]}, Room: {session[2]}, Division: {session[5]})")
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

        heading_style = ParagraphStyle(name="Heading", fontSize=20, alignment=1, spaceAfter=20)  # Center-aligned
        elements.append(Paragraph("<b>University Timetable</b>", style=heading_style))

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
    # Run the algorithm
    best_timetable = genetic_algorithm(pop_size=20, generations=100)
    generate_pdf_timetable(best_timetable)
    print("\nBest Timetable:")
    print_timetable(best_timetable)


# Sample data (IDs for simplicity)

def advanced_timetable_generation():
    import random

    # Sample data (IDs for simplicity)
    subjects = ["DSA",'spm','aj','mfcs','ecommerce','aj lab','wt lab','adbms','adbms lab']
    teachers = ['pankaj', 'neha', 'sanju', 'shilpa','anup','snehil','swasthi','roshna mam']
    rooms = ['102', '103', '001','002','003','004']

    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    time_slots = ['9-10', '10-11', '11-12', '12-1','1-3','3-5']  # 4 lectures per day
     # 4 lectures per day
    batches = ['A', 'B']
    practical_batches=["B1","B2","B3","B4"]
    # Mapping: (Subject, Division) → (Teacher, Room)
    subject_teacher_room = {
        ('adbms', 'A'): ('neha', '103'),
        ('spm', 'A'): ('anup', '103'),
        ('mfcs', 'A'): ('neha', '103'),
        ('DSA','B4'):('sanju','004'),
        ('DSA', 'B3'): ('shilpa', '003'),
        ('DSA',"B1"):("shilpa",'001'),
        ('ecommerce','A'):("sanju",'103'),
        ('ecommerce', 'B'): ('sanju', '102'),
        ('adbms', 'B'): ('neha', '102'),
        ('spm', 'B'): ('anup', '102'),
        ('mfcs', 'B'): ('snehil', '102'),
        ('aj', 'B'): ('pankaj', '102'),
        ('adbms lab', 'B2'): ('neha', '004'),
        ('adbms lab','B1'):('neha','003'),
        ('adbms lab','B3'):('swasthi','002'),
        ('adbms lab','B4'):('neha','001'),
        ('DSA',"B2"):('shilpa','002'),
        ('aj lab','B1'):('pankaj','001'),
        ('aj lab','B2'):('pankaj','003'),
        ('aj lab','B3'):('pankaj','002'),
        ('aj lab','B4'):('pankaj','004'),
        ('wt lab','B1'):('roshna','001'),
        ('wt lab', 'B2'):('roshna', '002'),
        ('wt lab','B3'):("roshna",'003'),
        ('wt lab','B4'):('anup','004'),

    }

    def create_gene(subject, division):
        teacher, room = subject_teacher_room[(subject, division)]
        return (subject, teacher, room, random.choice(days), random.choice(time_slots), division)

    # Chromosome: a complete timetable (list of genes)
    def create_chromosome():
        chromosome = []
        for division in batches:
            subjects_for_division = [subj for subj, div in subject_teacher_room if div == division]
            for day in days:
                daily_subjects = random.choices(subjects_for_division, k=2)  # 2 lectures per day for A/B
                for i, time_slot in enumerate(time_slots[:2]):
                    subject = daily_subjects[i]
                    chromosome.append(create_gene(subject, division)[:3] + (day, time_slot, division))

        # Assign synchronized practicals to practical batches
        practical_subjects = [subj for subj, div in subject_teacher_room if div in practical_batches]
        for day in days:
            practical_time_slot = random.choice(time_slots[2:])  # Assign to later slots
            selected_subjects = random.sample(practical_subjects, 4)
            for i, batch in enumerate(practical_batches):
                subject = selected_subjects[i % len(selected_subjects)]
                chromosome.append(create_gene(subject, batch)[:3] + (day, practical_time_slot, batch))
        return chromosome

    # Population: a collection of chromosomes
    def create_population(size):
        return [create_chromosome() for _ in range(size)]

    # Fitness Function: penalize conflicts
    def fitness(chromosome):
        score = 0
        seen = set()
        for gene in chromosome:
            key = (gene[1], gene[3], gene[4])  # (Teacher, Day, Time Slot)
            room_key = (gene[2], gene[3], gene[4])  # (Room, Day, Time Slot)
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
                subject = random.choice([subj for subj, div in subject_teacher_room if div == division])
                chromosome[i] = create_gene(subject, division)
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
            print(f"  {session[4]} - {session[0]} (Teacher: {session[1]}, Room: {session[2]}, Division: {session[5]})")
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

        heading_style = ParagraphStyle(name="Heading", fontSize=20, alignment=1, spaceAfter=20)  # Center-aligned
        elements.append(Paragraph("<b>University Timetable</b>", style=heading_style))

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
    # Run the algorithm
    best_timetable = genetic_algorithm(pop_size=20, generations=100)
    generate_pdf_timetable(best_timetable)
    print("\nBest Timetable:")
    print_timetable(best_timetable)


# advanced_timetable_generation()



def timetable_generator_for_therotical_batches(batchid,course,year):
    import random
    cur = conn.cursor()
    cur.execute("SELECT course_id FROM batch WHERE batch_id=(%s)", (batchid,))
    courseId = cur.fetchall()[0][0]
    cur.execute("SELECT teacher_name FROM teachers WHERE course_id=(%s)", (courseId,))
    teachers = [item[0] for item in cur.fetchall()]
    cur.execute(
        """SELECT st.subjectToTeacherID, s.subject_name, t.teacher_name, st.division, st.prac_batch, r.room_no FROM subjecttoteacher st JOIN subjects s ON st.subject_id = s.subject_id JOIN teachers t ON st.teacher_id = t.teacher_id JOIN rooms r ON st.room_id = r.room_id WHERE st.batch_id=(%s);""",
        (batchid,))
    subject_teacher_room_query = cur.fetchall()
    subject_teacher_room = transform_query_to_dictonary(subject_teacher_room_query)
    # for row in subject_teacher_room:
    #     print(row)
    cur.execute("""SELECT subject_id,subject_name,semester FROM subjects WHERE course_id=(%s)""", (courseId,))
    subjects = [item[1] for item in cur.fetchall()]
    cur.execute("""SELECT DISTINCT room_no FROM rooms""")
    rooms_query = [item[0] for item in cur.fetchall()]
    rooms = [str(num).zfill(3) for num in rooms_query]
    # # divisions
    cur.execute("SELECT DISTINCT division FROM subjecttoteacher WHERE division IS NOT NULL AND division <> '';")
    batches = [row[0] for row in cur.fetchall()]
    # cur.execute("SELECT DISTINCT prac_batch FROM subjecttoteacher WHERE prac_batch IS NOT NULL AND prac_batch <> '';")
    # practical_batches = [row[0] for row in cur.fetchall()]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    #
    time_slots = ['9-10', '10-11', '11-1', '1-3', '3-5']

    # Gene: (Subject, Teacher, Room, Day, Time Slot, Batch)
    def create_gene(subject, division):
        teacher, room = subject_teacher_room[(subject, division)]
        return (subject, teacher, room, random.choice(days), random.choice(time_slots), division)

    # Chromosome: a complete timetable (list of genes)
    def create_chromosome():
        chromosome = []
        division_time_slot = {day: {time_slot: [] for time_slot in time_slots} for day in days}

        for division in batches:
            subjects_for_division = [subj for subj, div in subject_teacher_room if div == division]
            for day in days:
                daily_subjects = random.sample(subjects_for_division, min(4, len(subjects_for_division)))
                for i, time_slot in enumerate(time_slots[:len(daily_subjects)]):
                    subject = daily_subjects[i]

                    # Ensure division does not repeat in the same time slot
                    while division in division_time_slot[day][time_slot]:
                        subject = random.choice([subj for subj, div in subject_teacher_room if div == division])

                    # Add to chromosome
                    chromosome.append(create_gene(subject, division)[:3] + (day, time_slot, division))
                    division_time_slot[day][time_slot].append(division)  # Track the division in this time slot

        return chromosome

    # Population: a collection of chromosomes
    def create_population(size):
        return [create_chromosome() for _ in range(size)]

    # Fitness Function: penalize conflicts
    def fitness(chromosome):
        score = 0
        seen = set()
        division_time_slot = set()  # Set to track divisions per time slot
        for gene in chromosome:
            teacher, day, time_slot, division = gene[1], gene[3], gene[4], gene[5]
            key = (teacher, day, time_slot)  # (Teacher, Day, Time Slot)
            room_key = (gene[2], day, time_slot)  # (Room, Day, Time Slot)
            batch_key = (division, day, time_slot)  # (Division, Day, Time Slot)

            # Penalize if teacher, room, or division conflicts
            if key in seen or room_key in seen or batch_key in seen:
                score -= 10  # Conflict
            else:
                seen.add(key)
                seen.add(room_key)
                seen.add(batch_key)

            # Check for division conflict in the same time slot
            if (division, day, time_slot) in division_time_slot:
                score -= 20  # Additional penalty for division conflict
            else:
                division_time_slot.add((division, day, time_slot))

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
                subject = random.choice([subj for subj, div in subject_teacher_room if div == division])
                chromosome[i] = create_gene(subject, division)
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
            print(f"  {session[4]} - {session[0]} (Teacher: {session[1]}, Room: {session[2]}, Division: {session[5]})")

    def generate_pdf_timetable(timetable, week_name="Week 1", filename=course+"_timetable.pdf"):

        # Sort timetable by day, division, and time slot
        timetable_sorted = sorted(timetable, key=lambda x: (days.index(x[3]), x[5], time_slots.index(x[4])))

        # Group sessions by day and division
        days_data = {day: {batch: [] for batch in batches} for day in days}
        for session in timetable_sorted:
            days_data[session[3]][session[5]].append(session)

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []

        # Add Week Name as centered heading
        heading_style = ParagraphStyle(name="Heading", fontSize=20, alignment=1, spaceAfter=20)  # Center-aligned
        elements.append(Paragraph(f"<b>{week_name}</b>", style=heading_style))

        # Add "University Timetable" heading
        elements.append(Paragraph("<b> " + course + "-" + str(year) + " Timetable </b>" , style=heading_style))

        # Add table for each weekday
        for day, divisions in days_data.items():
            elements.append(
                Paragraph(f"<b>{day}</b>", style=ParagraphStyle(name="Heading", fontSize=14, spaceAfter=10)))

            for division, sessions in divisions.items():
                if sessions:  # Only add division if there are sessions for that division
                    elements.append(
                        Paragraph(f"<b>Division {division}</b>",
                                  style=ParagraphStyle(name="Heading", fontSize=12, spaceAfter=10)))

                    # Prepare data for the table
                    data = [["Time Slot", "Subject", "Teacher", "Room"]]
                    for session in sessions:
                        data.append([session[4], session[0], session[1], session[2]])

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
                    elements.append(Spacer(1, 10))  # Add spacing after each division's table

                elements.append(Spacer(1, 20))  # Add spacing after each day

        # Build PDF
        doc.build(elements)
        print(f"PDF generated: {filename}")

    # Run the algorithm
    best_timetable = genetic_algorithm(pop_size=20, generations=100)
    generate_pdf_timetable(best_timetable)
    print("\nBest Timetable:")
    print_timetable(best_timetable)

# timetable_generator_for_therotical_batches()

# Sample data for theoretical-only courses (e.g., MBA, Commerce)
# subjects = [
#     'Economics', 'Accounting', 'Marketing', 'Management',
#     'Computer Science', 'Physics', 'Chemistry', 'Mathematics',
#     'Biology', 'History', 'Geography', 'Psychology', 'Sociology'
# ]
# teachers = [
#     'T001', 'T002', 'T003', 'T004', 'T005', 'T006', 'T007', 'T008',
#     'T009', 'T010', 'T011', 'T012', 'T013', 'T014', 'T015'
# ]
# rooms = ['R101', 'R102', 'R103', 'R104', 'R105', 'R106', 'R107', 'R108']
# days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
# time_slots = ['9-10', '10-11', '11-12', '12-1', '1-2', '2,3']  # 4 lectures per day
# batches = ['A', 'B', 'C', 'D']
#
# # Mapping: (Subject, Division) → (Teacher, Room)
# subject_teacher_room = {
#     ('Economics', 'A'): ('T001', 'R101'),
#     ('Accounting', 'A'): ('T002', 'R102'),
#     ('Marketing', 'B'): ('T003', 'R103'),
#     ('Management', 'B'): ('T004', 'R104'),
#     ('Computer Science', 'C'): ('T005', 'R105'),
#     ('Physics', 'C'): ('T006', 'R106'),
#     ('Chemistry', 'D'): ('T007', 'R107'),
#     ('Mathematics', 'D'): ('T008', 'R108'),
#     ('Biology', 'A'): ('T009', 'R101'),
#     ('History', 'B'): ('T010', 'R102'),
#     ('Geography', 'C'): ('T011', 'R103'),
#     ('Psychology', 'D'): ('T012', 'R104'),
#     ('Sociology', 'A'): ('T013', 'R105'),
#     ('Economics', 'B'): ('T014', 'R106'),
#     ('Marketing', 'C'): ('T015', 'R107'),
#     ('Management', 'D'): ('T001', 'R108'),
#     ('Computer Science', 'A'): ('T002', 'R101'),
#     ('Physics', 'B'): ('T003', 'R102'),
#     ('Chemistry', 'C'): ('T004', 'R103'),
#     ('Mathematics', 'A'): ('T005', 'R104'),
#     ('Biology', 'B'): ('T006', 'R105'),
#     ('History', 'C'): ('T007', 'R106'),
#     ('Geography', 'D'): ('T008', 'R107'),
#     ('Psychology', 'A'): ('T009', 'R108'),
#     ('Sociology', 'B'): ('T010', 'R101')
# }