# Usage :
# python main.py <nom fichier epub>

import os
import shutil
import zipfile
import argparse
import xml.etree.ElementTree as ET
import re

# Définition d'un argument de ligne de commande pour le chemin vers le fichier EPUB à décompresser
parser = argparse.ArgumentParser(
    description="Décompresser un fichier EPUB dans un dossier temporaire"
)
parser.add_argument(
    "epub_path", type=str, help="Chemin vers le fichier EPUB à décompresser"
)
args = parser.parse_args()
epub_path = args.epub_path

# Création d'un dossier temporaire pour extraire le contenu du fichier EPUB
tempDir = "./temp"
if not os.path.exists(tempDir):
    os.makedirs(tempDir)

# Extraction du fichier EPUB dans le dossier temporaire
with zipfile.ZipFile(epub_path, "r") as zipRef:
    zipRef.extractall(tempDir)

oebpsDir = "./temp/OEBPS"
for root, dirs, files in os.walk(oebpsDir):
    ET.register_namespace("", "http://www.idpf.org/2007/opf")
    for file in files:
        if file.endswith(".opf"):
            opfPath = os.path.join(root, file)
            with open(opfPath, "r") as f:
                opfContent = f.read()
            opfTree = ET.ElementTree(ET.fromstring(opfContent))
            metadata = opfTree.find("{http://www.idpf.org/2007/opf}metadata")
            if metadata is not None:
                balises = [
                    ("schema:accessibilitySummary", "Cet EPUB est accessible aux personnes en situation de handicap. Il respecte la charte du SNE (EPUB textuels nativement accessibles) et les spécifications du W3C (EPUB accessibility techniques, WCAG AA et ARIA)."),
                    ("schema:accessibilityHazard", "noFlashingHazard"),
                    ("schema:accessibilityHazard", "noMotionSimulationHazard"),
                    ("schema:accessibilityHazard", "noSoundHazard"),
                    ("schema:accessibilityFeature", "readingOrders"),
                    ("schema:accessibilityFeature", "structuralNavigation"),
                    ("schema:accessibilityFeature", "printPageNumbers"),
                    (
                        "a11y:certifierReport",
                        "Les résultats du contrôle qualité de l’accessibilité de cet EPUB peuvent être demandés à la maison d’édition.",
                    ),
                    (
                        "a11y:certifierCredential",
                        "Le commanditaire et le prestataire de cet EPUB ont été formés à l’ensemble des techniques d’accessibilité qui s’appliquent.",
                    ),
                    ("dcterms:conformsTo", "EPUB Accessibility 1.1 - WCAG 2.1 Level A"),
                    ("schema:accessibilityControl", "fullKeyboardControl"),
                    ("schema:accessibilityControl", "fullMouseControl"),
                    ("schema:accessibilityControl", "fullSwitchControl"),
                    ("schema:accessibilityControl", "fullTouchControl"),
                    ("schema:accessibilityAPI", "ARIA"),
                    ("schema:accessibilityFeature", "tableOfContents"),
                    ("schema:accessibilityFeature", "displayTransformability"),
                    ("ibooks:specified-fonts", "true"),
                    ("schema:accessMode", "textual"),
                    ("schema:accessMode", "visual"),
                    ("schema:accessModeSufficient", "textual"),
                    ("schema:accessibilityFeature", "alternativeText"),
                ]
                meta = None
                for balise in balises:
                    meta = ET.SubElement(metadata, "meta")
                    meta.set("property", balise[0])
                    meta.text = balise[1]
                    meta.tail = "\n"  # ajouter une nouvelle ligne après la balise

                    metadata.append(meta)

                with open(opfPath, "wb") as f:
                    opfTree.write(f, encoding="utf-8", xml_declaration=True)
            else:
                print("La balise metadata n'a pas été trouvée dans le fichier .opf.")
        elif file.endswith((".html")) and epub_path[:-5] in file:
            filename = os.path.splitext(file)[0]
            htmlPath = os.path.join(root, file)
            with open(htmlPath,  "r", encoding="utf-8") as f:
                content = f.read()
            match = re.search(r"<html\s*(.*?)>", content, re.DOTALL)
            if match:
                attributes = match.group(1)
                newHtml = f'<html xmlns:epub="http://www.idpf.org/2007/ops" xmlns="http://www.w3.org/1999/xhtml" xmlns:schema="http://schema.org/" xmlns:php="http://php.net/xsl" lang="fr-FR" xml:lang="fr-FR" {attributes}>'
                content = re.sub(r"<html\s*(.*?)>", newHtml, content, flags=re.DOTALL)
            else:
                content = re.sub(
                    r"<html>",
                    '<html xmlns:epub="http://www.idpf.org/2007/ops" xmlns="http://www.w3.org/1999/xhtml" xmlns:schema="http://schema.org/" xmlns:php="http://php.net/xsl" lang="fr-FR" xml:lang="fr-FR">',
                    content,
                )
            match = re.search(r"<body\s*(.*?)>", content, re.DOTALL)
            if match:
                attributes = match.group(1)
                newBody = f'<body lang="fr-FR" xml:lang="fr-FR"  id="' + filename + '">'
                content = re.sub(r"<body\s*(.*?)>", newBody, content, flags=re.DOTALL)
            else:
                content = re.sub(
                    r"<body>",
                    '<body lang="fr-FR" xml:lang="fr-FR">',
                    content,
                )
            with open(htmlPath, "w", encoding="utf-8") as f:
                f.write(content)

output_dir = "./output"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
shutil.make_archive("output", "zip", tempDir)
os.rename("output.zip", epub_path.replace(".epub", "") + "_modified.epub")
shutil.move(epub_path.replace(".epub", "") + "_modified.epub", output_dir)
shutil.rmtree(tempDir)
