 type Props = {
    conversations: any[];
    onSelectConversation: (conv: any) => void;
    onNewConversation:() => void;
    userId: string;
    
  }


export default function Sidebar({conversations, onSelectConversation,onNewConversation, userId}: Props) {
  
  return (
    <aside className="w-72 h-screen bg-zinc-900 text-white p-4 flex flex-col">

      <button
        onClick={onNewConversation}

        className="mb-4 bg-white text-black p-3 rounded-xl cursor-pointer font-medium hover:bg-zinc-200"
      >
        + New Chat
      </button>

      <h2 className="text-xl font-bold mb-4">
        Conversations
      </h2>

      <div className="flex-1 overflow-y-auto space-y-2 pr-1">
        {conversations.map((conv) => (
          <button
            key={conv.id}

            onClick={()=>
              onSelectConversation(conv)
            }

            className="w-full text-left p-3 rounded-lg cursor-pointer bg-zinc-800 hover:bg-zinc-700"
          >
            {conv.title}
          </button>
        ))}
      </div>

      <button
        className="mt-4 bg-zinc-800 hover:bg-zinc-700 p-3 rounded-xl cursor-pointer text-left">
      👤 {userId}
      </button>

    </aside>
  );
}