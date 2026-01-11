import React, { useState } from 'react';

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [answers, setAnswers] = useState({});

  async function upload() {
    if (!file) {
      alert('Please select a PDF file');
      return;
    }

    const f = new FormData();
    f.append('file', file);

    setLoading(true);
    setData(null);
    setAnswers({});

    try {
      const r = await fetch('http://127.0.0.1:5000/api/upload-pdf', {
        method: 'POST',
        headers: {
          Authorization: 'Bearer ' + sessionStorage.getItem('token')
        },
        body: f
      });

      const result = await r.json();
      setData(result);
    } catch (err) {
      alert('Failed to process PDF');
    } finally {
      setLoading(false);
    }
  }

  function selectAnswer(qIndex, option) {
    if (answers[qIndex]) return;
    setAnswers({ ...answers, [qIndex]: option });
  }

  return (
    <div className="container">
      <div className="card">
        <h2>Upload PDF</h2>

        <input
          type="file"
          accept="application/pdf"
          onChange={e => setFile(e.target.files[0])}
        />

        <button className="button" onClick={upload} disabled={loading}>
          {loading ? 'Processing...' : 'Process'}
        </button>
      </div>

      {data && (
        <>
          {/* SUMMARY */}
          <div className="card">
            <h2>Summary</h2>
            <p className="summary-text">{data.summary}</p>
          </div>

          {/* MCQS */}
          <div className="card">
            <h2>Practice Questions</h2>

            {data.mcqs.map((q, i) => (
              <div key={i} className="mcq">
                <p className="mcq-question">{q.question}</p>

                <div className="mcq-options">
                  {q.options.map((opt, j) => {
                    const chosen = answers[i];
                    const isCorrect = opt === q.answer;
                    const isChosen = chosen === opt;

                    let cls = 'mcq-option';
                    if (chosen) {
                      if (isCorrect) cls += ' correct';
                      else if (isChosen) cls += ' wrong';
                    }

                    return (
                      <div
                        key={j}
                        className={cls}
                        onClick={() => selectAnswer(i, opt)}
                      >
                        {opt}
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* FLASHCARDS */}
          <div className="card">
            <h2>Flashcards</h2>

            <div className="flashcards">
              {data.flashcards.map((f, i) => (
                <div key={i} className="flashcard">
                  <div className="flashcard-inner">
                    <div className="flashcard-front">
                      {f.question}
                    </div>
                    <div className="flashcard-back">
                      {f.answer}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
