import ChatInput from './ChatInput';

export default function ChatWindow() {
    const messages = [{ 
        role: 'user', 
        content: 'Hello, how are you?' 
    },
        { 
            role: 'assistant', 
            content: 'I am fine, thank you! How can I assist you today?' 
        }
    ];

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
              {msg.content}
            </div>

            </div>
                ))}
            </div>

            <ChatInput />
        </section>

    );

}