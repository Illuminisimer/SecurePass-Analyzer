import { type ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
}

export function Button({ variant = "primary", className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center rounded-3xl px-5 py-3 text-sm font-semibold transition",
        variant === "primary"
          ? "bg-brand-500 text-white shadow-soft hover:bg-brand-400"
          : "border border-slate-700 bg-slate-950 text-slate-100 hover:bg-slate-900",
        className,
      )}
      {...props}
    />
  );
}
