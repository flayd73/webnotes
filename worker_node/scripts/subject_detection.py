import os

def detect_subject_and_topic(transcript):
    # Define subjects and their topics
    subjects = {
        "chemistry": [
            "Acids, Bases & PH Calculations",
            "Atomic Structure",
            "Chemical Equilibrium",
            "Electron Arrangement",
            "Experiment Q1 (Titration)",
            "Experiment Q2 (Organic)",
            "Experiment Q3 (Other)",
            "Fuels & Thermochemistry",
            "Industrial Chemistry",
            "Materials & Polymers",
            "Metals",
            "Organic Chemistry",
            "Oxidation & Reduction",
            "Periodic Table",
            "Radioactivity",
            "Rates of Reaction",
            "Stoichiometry, Formulae & Equations",
            "Water & Water Analysis"
        ],
        "physics": [
            "Acceleration",
            "Applied Electricity",
            "Circular Motion",
            "Current & Charge",
            "Electric Circuits",
            "Electromagnetic Induction",
            "Exp. Qs (all)",
            "Exp. Qs. - Electricity",
            "Exp. Qs. - Heat",
            "Exp. Qs. - Light",
            "Exp. Qs. - Mechanics",
            "Exp. Qs. - Sound",
            "Force, Mass & Momentum",
            "Heat & Heat Transfer",
            "Light",
            "Magnets & Magnetic Fields",
            "Nuclear Energy",
            "Particle Physics",
            "Potential Difference & Capacitance",
            "Pressure, Gravity & Moments",
            "Reflection & Mirrors",
            "Refraction & Lenses",
            "Resistance",
            "Semiconductors",
            "Simple Harmonic Motion",
            "Speed, Displacement, Velocity",
            "Static Electricity",
            "Temperature & Thermometers",
            "The Atom, Nucleus & Radioactivity",
            "The Electron",
            "Vectors & Scalars",
            "Vibration & Sound",
            "Waves & Wave Motion",
            "Work, Energy & Power"
        ],
        "biology": [
            "Bacteria",
            "Blood & Circulatory System",
            "Breathing System",
            "Cell Division",
            "Cell Metabolism & Enzymes",
            "Cell Structure",
            "Characteristics of Life",
            "Digestive System",
            "Ecology",
            "Excretion",
            "Experiment Questions",
            "Eye and Ear",
            "Food & Food tests",
            "Fungi",
            "Genetics, DNA & Evolution",
            "Hormonal/Endocrine System",
            "Human Reproduction",
            "Immune system",
            "Movement Through Cell Membranes",
            "Musculoskeletal System",
            "Nervous System",
            "Photosynthesis",
            "Plant Reproduction",
            "Plant Responses",
            "Plant Structure",
            "Plant Transport",
            "Protista",
            "Respiration",
            "The Scientific Method",
            "The Study of an Ecosystem",
            "Viruses"
        ]
    }
    transcript_lower = transcript.lower()
    # Detect subject and topic
    for subject, topics in subjects.items():
        for topic in topics:
            if topic.lower() in transcript_lower:
                return subject, topic
    # If no specific subject and topic are found, return None
    return None, "General"

def find_syllabus(subject, resources_path):
    for file_name in os.listdir(resources_path):
        if subject.lower() in file_name.lower() and file_name.lower().endswith(".pdf"):
            return os.path.join(resources_path, file_name)
    return None