import { useState, useRef } from "preact/hooks";
import { JSX } from "preact";

// Dummy data for mention suggestions
const MENTION_SUGGESTIONS = [
  { id: "user1", name: "Alice" },
  { id: "user2", name: "Bob" },
  { id: "user3", name: "Charlie" },
  { id: "user4", name: "David" },
];

export default function MentionTextbox() {
  const [text, setText] = useState("");
  const [showSuggestions, setShowSuggestions] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleInput = (e: JSX.TargetedEvent<HTMLTextAreaElement>) => {
    const textarea = e.currentTarget;
    const newText = textarea.value;
    setText(newText);

    const cursorPos = textarea.selectionStart;
    const textBeforeCursor = newText.substring(0, cursorPos);
    const lastAt = textBeforeCursor.lastIndexOf("@");

    // Show suggestions if '@' is typed and there's no space after it
    if (lastAt !== -1 && !textBeforeCursor.substring(lastAt + 1).includes(" ")) {
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (name: string) => {
    if (!textareaRef.current) return;

    const textarea = textareaRef.current;
    const cursorPos = textarea.selectionStart;
    const textBeforeCursor = text.substring(0, cursorPos);
    const lastAt = textBeforeCursor.lastIndexOf("@");

    const textBeforeAt = text.substring(0, lastAt);
    const textAfterCursor = text.substring(cursorPos);

    const newText = `${textBeforeAt}@${name} ${textAfterCursor}`;
    setText(newText);
    setShowSuggestions(false);

    // Move cursor to after the inserted mention
    setTimeout(() => {
      textarea.focus();
      const newCursorPos = `${textBeforeAt}@${name} `.length;
      textarea.setSelectionRange(newCursorPos, newCursorPos);
    }, 0);
  };

  return (
    <div class="relative w-full">
      <textarea
        ref={textareaRef}
        value={text}
        onInput={handleInput}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 100)} // Hide on blur with a delay
        class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Type @ to mention someone..."
        rows={4}
      />
      {showSuggestions && (
        <div class="absolute z-10 w-48 bg-white border border-gray-200 rounded-md shadow-lg mt-1">
          <ul class="py-1">
            {MENTION_SUGGESTIONS.map((user) => (
              <li
                key={user.id}
                class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
                onMouseDown={() => handleSuggestionClick(user.name)}
              >
                {user.name}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}