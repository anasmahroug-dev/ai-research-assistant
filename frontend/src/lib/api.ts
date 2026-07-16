import { APP_DIR_ALIAS } from "next/dist/lib/constants";
import Stream from "stream";
import {PDF} from "@/types"

export const API_URL = 
process.env.NEXT_PUBLIC_API_URL ??
"http://localhost:8000";


export type StreamEvent =
    | {
          type: "token";
          data: string;
      }
    | {
          type: "update";
          data: string;
      }
    | {
          type: "done";
      };


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
    onEvent: (event: StreamEvent) => void){

        const response = await fetch(
            `${API_URL}/chat/`,
            {
                method: "POST",
                headers:authHeaders(true),

                body: JSON.stringify({conversation_id: conversationId,
                    message,}),


            }
        );

        const reader = response.body?.getReader();

        if (!reader) return;
        const decoder = new TextDecoder();
        let buffer = "";
        while (true){
            const {done, value} = await reader.read();
            if (done) break;
            buffer += decoder.decode(value, {stream: true});

            const events = buffer.split("\n\n");
            buffer = events.pop() ?? "";

            for (const eventText of events){
                const lines = eventText.split("\n");

                const event =
                lines.find(l => l.startsWith("event:"))
                ?.replace("event:", "")
                .trim();

                const data = lines
                .filter(l => l.startsWith("data:"))
                .map(l => l.slice(5).trimStart())
                .join("\n");

                if (!event || data === undefined) continue;
                
                console.log("RAW:", data);
                const parsed = JSON.parse(data);
                console.log(typeof parsed);
                console.log(parsed);
                console.log(JSON.stringify(parsed));

                switch (event) {
                    case "token":
                        onEvent({
                            type: "token",
                            data: parsed,
                        });
                        break;

                    case "update":
                        onEvent({
                            type: "update",
                            data: parsed,
                        });
                        break;

                    case "done":
                        onEvent({
                            type: "done",
                        });
                        break;
                }
            }
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

export async function getPdfs(conversationId: number): Promise<PDF[]> {

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