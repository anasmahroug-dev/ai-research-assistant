import { APP_DIR_ALIAS } from "next/dist/lib/constants";

const API_URL = "http://localhost:8000";

function authHeaders(contentType = false) {
    const token = localStorage.getItem("token");

    return {
        ...(contentType && { "Content-Type": "application/json" }),
        Authorization: `Bearer ${token}`,
    };
}

export async function getConversations()
{

    const response = await fetch(
        `${API_URL}/conversations/`,{
        headers: authHeaders(),
        }

    );
    return response.json();
}

export async function createConversation(){
 
    
    const response = await fetch(
        `${API_URL}/conversations/`,
        {
            method: "POST",
            headers: authHeaders(),
        }
    );
    return response.json();
}

export async function getMessages(conversationId: number){
    const response = await fetch(
        `${API_URL}/chat/history/${conversationId}`,
        {headers: authHeaders()}
    );
    return response.json();
}



export async function sendMessageStream(conversationId: number, message: string, 
    onChunk: (chunk: string)=> void){

        const response = await fetch(
            `${API_URL}/chat/`,
            {
                method: "POST",
                headers:authHeaders(true),

                body: JSON.stringify({conversation_id: conversationId,
                    message,}),


            }
        );
        const text = await response.clone().text();

        console.log(response.status);
        console.log(text);
        const reader = response.body?.getReader();

        if (!reader) return;
        const decoder = new TextDecoder();
        while (true){
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value);
            onChunk(chunk);
        }

}


export async function uploadPDF(conversationId: number, file: File){

    const formData = new FormData();

    formData.append("conversation_id", String(conversationId));

    formData.append("file", file);

    const response= await fetch(
        `${API_URL}/pdf/upload`,
        {
            method: "POST",
            headers: authHeaders(),
            body: formData,
        }
    );
    return response.json();
}

export async function getPdfs(conversationId: number) {

  const response = await fetch(
    `${API_URL}/pdf/${conversationId}`, {
        headers: authHeaders(),
    }
  );

  return response.json();
}

export async function deleteConversation(conversationId: number){

    const response = await fetch(
        `${API_URL}/conversations/${conversationId}`,
        {
            method: "DELETE",
            headers: authHeaders(),
        }
    );
    return response.json();

}

export async function renameConversation(conversationId: number, title: string){
    const response = await fetch(
        `${API_URL}/conversations/${conversationId}?title=${encodeURIComponent(title)}`,
        {
            method: "PUT",
            headers: authHeaders(),
        }
    );

    return response.json();


}

export async function getChunk(chunkId: number){
    const response = await fetch(
        `${API_URL}/chunks/${chunkId}`,{
            headers: authHeaders(),
        }
    )

    return response.json();

}

export async function deletePdf(pdfId: number){
    const response = await fetch(
        `${API_URL}/pdf/${pdfId}`,
        {
        method:"DELETE",
        headers: authHeaders(),
        }
    );

    return response.json();

}