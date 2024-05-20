import * as React from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement | HTMLTextAreaElement> {
  as?: "input" | "textarea";
}

const Input = React.forwardRef<HTMLInputElement | HTMLTextAreaElement, InputProps>(
  ({ className, as = "input", ...props }, ref) => {
    const inputRef = React.useRef<HTMLInputElement | HTMLTextAreaElement | null>(null);

    React.useImperativeHandle(ref, () => inputRef.current!);

    const handleInput = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
      const textArea = event.target;
      textArea.style.height = "auto"; // Reset height to auto to calculate the new height
      textArea.style.height = `${textArea.scrollHeight}px`; // Set the height to match the scroll height
    };

    return as === "textarea" ? (
      <textarea
        className={cn(
          "flex w-full max-h-40 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 resize-none overflow-auto",
          className
        )}
        ref={inputRef as React.Ref<HTMLTextAreaElement>}
        onInput={handleInput}
        {...(props as React.TextareaHTMLAttributes<HTMLTextAreaElement>)}
      />
    ) : (
      <input
        type={props.type}
        className={cn(
          "flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
          className
        )}
        ref={inputRef as React.Ref<HTMLInputElement>}
        {...props}
      />
    );
  }
);

Input.displayName = "Input";

export { Input };
