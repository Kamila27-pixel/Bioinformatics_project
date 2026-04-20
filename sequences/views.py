from django.shortcuts import render
from .algorithms import DNATrie
from .ml_logic import DNAClassifier
from .utils import generate_dna_chart
from Bio import SeqIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.http import HttpResponse
from Bio.Seq import Seq
from Bio.Restriction import Analysis, CommOnly, AllEnzymes
import io

KNOWN_MARKERS = ["ATGC", "GCTAG", "TTAA", "CCGG"]
trie = DNATrie()
for marker in KNOWN_MARKERS:
    trie.insert(marker)

clf = DNAClassifier()

def home_page(request):
    query = request.GET.get('q', '')
    result_text = ""
    ml_prediction = ""
    chart_data = ""
    protein_seq = ""
    restriction_results = []

    if request.method == 'POST' and request.FILES.get('fasta_file'):
        fasta_file = request.FILES['fasta_file']
        file_content = fasta_file.read().decode('utf-8')
        fasta_io = io.StringIO(file_content)

        for record in SeqIO.parse(fasta_io, "fasta"):
            query = str(record.seq).upper()
            break

    elif request.GET.get('q'):
        query = request.GET.get('q').upper()
    
    if query:
        exists = trie.search(query)
        result_text = f"Sequence (length {len(query)}) analyzed. Marker match: {'Yes' if exists else 'No'}"
        ml_prediction = clf.predict_coding(query)
        chart_data = generate_dna_chart(query)

        try:
            protein_seq = str(Seq(query).translate(to_stop=True))
        except Exception:
            protein_seq = "Error in translation"

        try:
            dna_obj = Seq(query)
            rb = Analysis(CommOnly, dna_obj)
            full_results = rb.mapping()

            for enzyme, cuts in full_results.items():
                if cuts:
                    restriction_results.append(f"{enzyme}: {cuts}")
        except:
            restriction_results = ["Error in restriction analysis"]
    
    return render(request, 'home.html', {
        'result': result_text,
        'ml_result': ml_prediction,
        'chart': chart_data,
        'query': query,
        'protein': protein_seq,
        'restriction': restriction_results
    })

def export_pdf(request):
    query = request.GET.get('q', '').upper()

    if not query:
        return HttpResponse("No sequence provided for PDF generation")
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-disposition'] = f'attachment; filename="BioInference_Report.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFillColor(colors.dodgerblue)
    p.rect(0, height - 80, width, 80, fill=1)
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 22)
    p.drawString(50, height - 50, "BioInference AI - analysis report")

    p.setFillColor(colors.black)
    p.setFont("Helvetica", 10)
    p.drawString(50, height - 100, f"Date: 2026-04-10")
    p.drawString(50, height - 115, f"Sequence length: {len(query)} bp")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 150, "1. DNA sequence preview")
    p.line(50, height - 155, 550, height - 155)
    p.setFont("Courier", 10)
    p.drawString(50, height - 175, query[:80] + ("..." if len(query) > 80 else ""))

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 210, "2. AI prediction")
    p.line(50, height - 215, 550, height - 215)
    p.setFont("Helvetica", 12)
    prediction = clf.predict_coding(query)
    p.drawString(60, height - 235, f"Coding potential: {prediction}")

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 270, "3. Protein sequence")
    p.line(50, height - 275, 550, height - 275)
    protein = str(Seq(query).translate(to_stop=True))
    p.setFont("Courier-Bold", 11)
    p.setFillColor(colors.magenta)
    p.drawString(60, height - 295, protein[:65] + ("..." if len(protein) > 65 else ""))

    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, height - 330, "4. Restriction sites")
    p.line(50, height - 335, 550, height - 335)
    p.setFont("Helvetica", 10)
    
    rb = Analysis(CommOnly, Seq(query))
    cuts = rb.mapping()
    y_pos = height - 355
    count = 0
    for enzyme, pos in cuts.items():
        if pos and count < 10:
            p.drawString(70, y_pos, f"- {enzyme}: {pos}")
            y_pos -= 15
            count += 1

    p.showPage()
    p.save()
    return response