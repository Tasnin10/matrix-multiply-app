from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML template for the input form
FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Matrix Multiplier</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .matrix-input { margin: 10px 0; }
        .error { color: red; }
        .result { margin-top: 20px; border: 2px solid #333; padding: 15px; display: inline-block; }
        .result pre { margin: 0; }
    </style>
</head>
<body>
    <h1>Matrix Multiplier</h1>
    <form method="POST" action="/multiply">
        <h3>Matrix A</h3>
        <div class="matrix-input">
            <label>Rows: <input type="number" name="rows_a" min="1" required value="{{ rows_a }}"></label>
            <label>Columns: <input type="number" name="cols_a" min="1" required value="{{ cols_a }}"></label>
        </div>
        <div>
            <label>Enter Matrix A (space-separated, row by row):</label><br>
            <textarea name="matrix_a" rows="5" cols="30" required>{{ matrix_a }}</textarea>
        </div>
        <h3>Matrix B</h3>
        <div class="matrix-input">
            <label>Rows: <input type="number" name="rows_b" min="1" required value="{{ rows_b }}"></label>
            <label>Columns: <input type="number" name="cols_b" min="1" required value="{{ cols_b }}"></label>
        </div>
        <div>
            <label>Enter Matrix B (space-separated, row by row):</label><br>
            <textarea name="matrix_b" rows="5" cols="30" required>{{ matrix_b }}</textarea>
        </div>
        <button type="submit">Multiply Matrices</button>
    </form>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    {% if result %}
        <div class="result">
            <h3>Result Matrix:</h3>
            <pre>{{ result }}</pre>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(FORM_TEMPLATE, rows_a='', cols_a='', matrix_a='', rows_b='', cols_b='', matrix_b='')

@app.route('/multiply', methods=['POST'])
def multiply_matrices():
    try:
        # Get form data
        rows_a = request.form['rows_a']
        cols_a = request.form['cols_a']
        matrix_a_input = request.form['matrix_a'].strip()
        rows_b = request.form['rows_b']
        cols_b = request.form['cols_b']
        matrix_b_input = request.form['matrix_b'].strip()

        # Convert dimensions to integers for validation
        rows_a_int = int(rows_a)
        cols_a_int = int(cols_a)
        rows_b_int = int(rows_b)
        cols_b_int = int(cols_b)

        # Validate matrix multiplication condition
        if cols_a_int != rows_b_int:
            return render_template_string(
                FORM_TEMPLATE,
                error="Columns of Matrix A must equal rows of Matrix B",
                rows_a=rows_a, cols_a=cols_a, matrix_a=matrix_a_input,
                rows_b=rows_b, cols_b=cols_b, matrix_b=matrix_b_input
            )

        # Parse matrix A
        matrix_a = [float(x) for x in matrix_a_input.split()]
        if len(matrix_a) != rows_a_int * cols_a_int:
            return render_template_string(
                FORM_TEMPLATE,
                error="Invalid number of elements in Matrix A",
                rows_a=rows_a, cols_a=cols_a, matrix_a=matrix_a_input,
                rows_b=rows_b, cols_b=cols_b, matrix_b=matrix_b_input
            )

        # Parse matrix B
        matrix_b = [float(x) for x in matrix_b_input.split()]
        if len(matrix_b) != rows_b_int * cols_b_int:
            return render_template_string(
                FORM_TEMPLATE,
                error="Invalid number of elements in Matrix B",
                rows_a=rows_a, cols_a=cols_a, matrix_a=matrix_a_input,
                rows_b=rows_b, cols_b=cols_b, matrix_b=matrix_b_input
            )

        # Convert to 2D arrays
        matrix_a_2d = [matrix_a[i * cols_a_int:(i + 1) * cols_a_int] for i in range(rows_a_int)]
        matrix_b_2d = [matrix_b[i * cols_b_int:(i + 1) * cols_b_int] for i in range(rows_b_int)]

        # Multiply matrices
        result = [[int(sum(a * b for a, b in zip(row_a, col_b))) for col_b in zip(*matrix_b_2d)] for row_a in matrix_a_2d]

        # Format result as a string for display
        result_str = '\n'.join([' '.join(map(str, row)) for row in result])

        # Render template with form data preserved
        return render_template_string(
            FORM_TEMPLATE,
            result=result_str,
            rows_a=rows_a, cols_a=cols_a, matrix_a=matrix_a_input,
            rows_b=rows_b, cols_b=cols_b, matrix_b=matrix_b_input
        )

    except ValueError:
        return render_template_string(
            FORM_TEMPLATE,
            error="Invalid input. Please enter valid numbers.",
            rows_a=rows_a, cols_a=cols_a, matrix_a=matrix_a_input,
            rows_b=rows_b, cols_b=matrix_b_input
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)