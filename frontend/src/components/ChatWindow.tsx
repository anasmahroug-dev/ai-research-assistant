import ChatInput from './ChatInput';    
import MessageContent from "./MessageContent";
import {LoaderCircle} from "lucide-react";

type Props ={
    messages: any[];
    onSend:(message: string) => void;
    onUploadPdf:(file: File) => void;
    isLoading: boolean;
    onCitationClick?: (filename: string, pages: number[], chunkId: number) => void | Promise<void>;
    className?: string;
    };

export default function ChatWindow({messages, onSend, onUploadPdf, isLoading, onCitationClick, className=""}: Props) {
    
    return (
        <section className={`flex flex-col bg-zinc-950 text-white min-h-0 ${className}`}>
            <div className="flex-1 min-h-0 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, index) => (
                    <div 
                key={index}
            className={msg.role === "user" 
                ? "flex justify-end"
                : "flex justify-start"
            }
            >
                 <div className="bg-zinc-800 p-4 rounded-xl max-w-xl">
                    <MessageContent
                        content={msg.message}
                        onCitationClick={onCitationClick}
                        />
                 </div>

            </div>
                ))}
            {isLoading && (
                <div className="flex justify-start">
                    
                    <div  
                    className="
                    flex 
                    items-center 
                    gap-2
                    bg-zinc-800
                    p-4
                    rounded-xl
                    max-w-xl">
                        <LoaderCircle size={20}className="animate-spin text-zinc-400"/>
                        <span className="text-zinc-400 text-sm">Thinking...</span>

                    </div>
                    
                </div>
            )}

            </div>

            <ChatInput onSend={onSend} onUploadPdf={onUploadPdf}/>
        </section>

    );

}