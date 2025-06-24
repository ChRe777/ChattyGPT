// Constants
//
const API_DOCS_QUERY = 'http://localhost:5050/api/docs/query';

export async function queryDocs(query) {

    const response = await fetch(API_DOCS_QUERY, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            query: query
        })
    })

    const result = await response.json();
    return result.documents
}
