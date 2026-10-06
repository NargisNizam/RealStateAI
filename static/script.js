// ---------------------------------------------
// Recommendation Form
// ---------------------------------------------

const recommendationForm =
    document.getElementById("recommendationForm");

const recommendationResults =
    document.getElementById("recommendationResults");


recommendationForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        recommendationResults.innerHTML =
            "<p>Searching properties...</p>";

        const formData =
            new FormData(recommendationForm);

        try {

            const response = await fetch(
                "/api/recommend",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data =
                await response.json();

            if (!data.success) {

                recommendationResults.innerHTML =
                    `<p>Error: ${data.error}</p>`;

                return;
            }

            recommendationResults.innerHTML = "";

            data.recommendations.forEach(
                (property, index) => {

                    const card =
                        document.createElement("div");

                    card.className =
                        "result-card";

                    card.innerHTML = `
                        <h3>
                            Property #${index + 1}
                        </h3>

                        <p>
                            <strong>Type:</strong>
                            ${property.type}
                        </p>

                        <p>
                            <strong>City:</strong>
                            ${property.city}
                        </p>

                        <p>
                            <strong>Location:</strong>
                            ${property.location}
                        </p>

                        <p>
                            <strong>Bedrooms:</strong>
                            ${property.bedrooms}
                            &nbsp; | &nbsp;
                            <strong>Bathrooms:</strong>
                            ${property.bathrooms}
                        </p>

                        <p>
                            <strong>Area:</strong>
                            ${property.area_marla} Marla
                        </p>

                        <p>
                            <strong>Price:</strong>
                            PKR ${Number(
                                property.price_pkr
                            ).toLocaleString()}
                        </p>

                        <p>
                            <strong>Why recommended:</strong>
                            ${property.reason}
                        </p>
                    `;

                    recommendationResults
                        .appendChild(card);
                }
            );

        } catch (error) {

            recommendationResults.innerHTML =
                `<p>Error connecting to server.</p>`;

        }

    }
);


// ---------------------------------------------
// AI Assistant
// ---------------------------------------------

const aiForm =
    document.getElementById("aiForm");

const aiResult =
    document.getElementById("aiResult");


aiForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        aiResult.innerHTML =
            "Thinking...";

        const formData =
            new FormData(aiForm);

        try {

            const response = await fetch(
                "/api/ai-assistant",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data =
                await response.json();

            if (!data.success) {

                aiResult.innerHTML =
                    `Error: ${data.error}`;

                return;
            }

            aiResult.innerHTML =
                data.answer;

        } catch (error) {

            aiResult.innerHTML =
                "Error connecting to AI assistant.";

        }

    }
);


// ---------------------------------------------
// RAG Assistant
// ---------------------------------------------

const ragForm =
    document.getElementById("ragForm");

const ragResult =
    document.getElementById("ragResult");


ragForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();

        ragResult.innerHTML =
            "Searching knowledge base...";

        const formData =
            new FormData(ragForm);

        try {

            const response = await fetch(
                "/api/rag",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data =
                await response.json();

            if (!data.success) {

                ragResult.innerHTML =
                    `Error: ${data.error}`;

                return;
            }

            let html =
                `<strong>Answer</strong><br><br>
                ${data.answer}`;

            if (
                data.sources &&
                data.sources.length > 0
            ) {

                html +=
                    "<br><br><strong>Sources:</strong><br>";

                data.sources.forEach(
                    source => {

                        html +=
                            `<span class="source">
                                ${source}
                            </span>`;

                    }
                );

            }

            ragResult.innerHTML = html;

        } catch (error) {

            ragResult.innerHTML =
                "Error connecting to RAG assistant.";

        }

    }
);