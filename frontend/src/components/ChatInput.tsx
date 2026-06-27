export default function ChatInput() {
  return (
    <div className="p-4 border-t border-zinc-800">
      <form className="flex gap-2">
         <label
          className="bg-zinc-800 px-4 py-3 rounded-xl cursor-pointer hover:bg-zinc-700"
        >
          📎 Upload .pdf

          <input
            type="file"
            accept=".pdf"
            className="hidden"
          />
        </label>
        
        <input
          type="text"
          placeholder="Ask something..."
          className="flex-1 bg-zinc-800 text-white p-4 rounded-xl outline-none"
        />

        <button
          className="bg-white text-black px-6 rounded-xl"
        >
          Send
        </button>
      </form>
    </div>
  );
}