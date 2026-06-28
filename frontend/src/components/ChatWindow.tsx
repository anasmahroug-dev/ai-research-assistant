import ChatInput from './ChatInput';    


type Props ={
    messages: any[];
    onSend:(message: string) => void;
    onUploadPdf:(file: File) => void;

};

export default function ChatWindow({messages, onSend, onUploadPdf}: Props) {
    
    

    return (
        <section className="flex-1 flex flex-col bg-zinc-950 text-white">
            <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, index) => (
                    <div 
                key={index}
            className={msg.role === "user" 
                ? "flex justify-end"
                : "flex justify-start"
            }
            >
                 <div className="bg-zinc-800 p-4 rounded-xl max-w-xl">
                    {msg.message}
                 </div>

            </div>
                ))}
            </div>

            <ChatInput onSend={onSend} onUploadPdf={onUploadPdf}/>
        </section>

    );

}