"use client";

import {useState} from "react";

type Props ={
onSend:(message: string) => void;
onUploadPdf:(file: File) => void;
};


export default function ChatInput({onSend, onUploadPdf}: Props) {

  const [input, setInput] = useState("");

  function handleSubmit(
    e: React.SyntheticEvent
  ){
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input);
    setInput("");
  }



  return (
    <div className="p-4 border-t border-zinc-800">
      <form 
      onSubmit={handleSubmit}
      className="flex gap-2">
         <label
          className="bg-zinc-800 px-4 py-3 rounded-xl cursor-pointer hover:bg-zinc-700"
        >
          📎 Upload pdf

          <input
            type="file"
            accept=".pdf"
            className="hidden"

            onChange={(e)=> {
              const file = e.target.files?.[0];
              console.log("FILE INPUT CHANGED");
              
              if(file){
                onUploadPdf(file);
              }
            }}
          />
        </label>
        
        <input
          value={input}
          onChange={(e)=>
            setInput(e.target.value)
          }

          type="text"
          placeholder="Ask something..."
          className="flex-1 bg-zinc-800 text-white p-4 rounded-xl outline-none"
        />

        <button
          className="bg-white text-black px-6 rounded-xl cursor-pointer"
        >
          Send
        </button>
      </form>
    </div>
  );
}