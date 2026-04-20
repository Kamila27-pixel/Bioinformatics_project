import plotly.graph_objects as go
import plotly.io as pio

def generate_dna_charts(sequence):
    seq = sequence.upper()
    labels = ['A', 'C', 'G', 'T']
    counts = [seq.count(n) for n in labels]

    fig = go.Figure(data=[
        go.Bar(
            x=labels,
            y=counts,
            marker_color=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'],
            hovertemplate="Nucleotide: %{x}<br>Count: %{y}<extra></extra>"
        )
    ])

    fig.update_layout(
        title=f"Nucleotide composition (Total length: {len(seq)})",
        xaxis_title="Nucleotide",
        yaxis_title="Count",
        template="plotly_white",
        height=400,
        font=dict(family="Arial, sans-serif", size=14)
    )

    return pio.to_html(fig, full_html=False, include_plotlyjs='cdn')