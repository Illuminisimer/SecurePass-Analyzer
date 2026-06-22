import { type ReactNode } from "react";
import { cn } from "@/lib/utils";

interface CardProps {
  children: ReactNode;
  className?: string;
}

export function Card({ children, className }: CardProps) {
  return (
    <div className={cn("rounded-3xl border border-slate-800 bg-slate-900/90 p-6 shadow-soft", className)}>
      {children}
    </div>
  );
}
