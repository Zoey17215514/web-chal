from flask import Flask, request, render_template_string

app = Flask(__name__)

# Make it EASY: flag is in config (no filesystem gymnastics)
app.config["FLAG"] = "tarumtFLAG{i_love_pineapple}"

@app.route("/")
def index():
    return """
    <h1>Template Trouble — Easy</h1>
    <p>Try the <a href="/search">search</a>. Tip: Does <code>{{7*7}}</code> evaluate?</p>
    """

@app.route("/search")
def search():
    q = request.args.get("q", "")
    # Intentionally vulnerable: user input becomes template SOURCE
    template = """
    <h2>Search results for: {{q}}</h2>
    <form action="/search" method="get">
      <input name="q" placeholder="search..." value="{{q}}">
      <button type="submit">Search</button>
    </form>
    <p>Hint: Sometimes configs hold secrets.</p>
    """
    # SUPER VULN: directly splicing user input into the template text
    return render_template_string(template.replace("{{q}}", q), q=q)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
