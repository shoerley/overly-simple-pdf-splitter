import PyPDF2
import csv
import sys
import random
import string
import os

"""
    Cet utilitaire a été partiellement créé à l'aide de ChatGPT
    20 février 2025
"""


def file_exists(file_path):
    return os.path.isfile(file_path)


def create_directory(name):
    if os.path.exists(name):
        raise FileExistsError(f"Le dossier '{name}' existe déjà.")
    os.makedirs(name)


def generate_folder_name(length=5):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def parse_csv(file_path, add_ext=".pdf"):
    """
    Lit un fichier CSV et retourne deux listes :
    - Une liste des premiers éléments de chaque ligne (chaînes de caractères).
    - Une liste de tuples contenant les deux valeurs numériques restantes.

    :param file_path: str, chemin vers le fichier CSV.
    :return: tuple (list[str], list[tuple[int, int]])
    """
    filenames = []
    intervals = []

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 3:  # Vérifier qu'on a au moins trois éléments par ligne

                filenames.append(row[0] + add_ext)
                intervals.append((int(row[1]), int(row[2])))

    return filenames, intervals


def split_pdf_by_intervals(pdf_path, intervals, output_prefix="output", output_folder=None, output_filenames=None):
    """
    Découpe un fichier PDF en plusieurs fichiers selon les intervalles de pages spécifiés.

    :param pdf_path: str, chemin du fichier PDF source.
    :param intervals: list of tuples, liste d'intervalles (début, fin), inclusifs et basés sur 1.
    :param output_prefix: str, préfixe des fichiers de sortie (par défaut 'output').
    """

    if output_folder is None:
        output_folder = "./" + generate_folder_name() + "_split"

    if output_folder[-1] != '/':
        output_folder += '/'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Ouvrir le fichier PDF
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)

        # Vérifier que les intervalles sont valides
        num_pages = len(reader.pages)
        for start, end in intervals:
            if start < 1 or end > num_pages or start > end:
                raise ValueError(f"Intervalle invalide: ({start}, {end}) pour un PDF de {num_pages} pages.")

        # Créer les fichiers PDF pour chaque intervalle
        for i, (start, end) in enumerate(intervals):
            writer = PyPDF2.PdfWriter()

            for page_num in range(start - 1, end):  # Convertir en index 0-based
                writer.add_page(reader.pages[page_num])

            if output_filenames is None:
                output_path_file = f"{output_folder + output_prefix}_part{i + 1}.pdf"
            else:
                output_path_file = f"{output_folder + output_filenames[i]}"

            if file_exists(output_path_file):
                raise FileExistsError(f"Le fichier {output_path_file} existe déjà et ne sera pas ré-écrit.")

            with open(output_path_file, "wb") as output_file:
                writer.write(output_file)

            print(f"Fichier généré: {output_path_file}")




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Script de division de fichier PDF")
        print("Usage: python pdfsplitter.py input_file.pdf split_config.csv <output_folder:str>")
        print("Le fichier input_file.pdf est le PDF qu'on veut diviser en plusieurs fichiers.")
        print("Le fichier splitconfig.csv contient la configuration d'un fichier de sortie par ligne :")
        print("\tnom du fichier, page_debut, page_fin")
        print("Par exemple : ")
        print("\tdétail des ventes, 18, 21")
        print("Les numéros de page de début et de fin sont tous les deux inclus.")
        print("Remarques")
        print("\t- Si aucun dossier de sortie n'est spécifié, un dossier est créé")
        print("\t- Si les fichiers à créer existent déjà à l'emplacement à écrire, ils ne sont pas réécrits")
    else:

        file_names, intervals = parse_csv(sys.argv[2])
        input_file = sys.argv[1]

        if len(sys.argv) == 4:
            output_folder = sys.argv[3]
        else:
            output_folder = None

        split_pdf_by_intervals(input_file, intervals=intervals, output_folder=output_folder,
                               output_filenames=file_names)

