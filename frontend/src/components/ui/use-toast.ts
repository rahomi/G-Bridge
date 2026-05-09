import * as React from "react";
import type { ToastProps } from "./toast";

type ToastActionElement = React.ReactElement;

type ToastOptions = {
  title?: string;
  description?: string;
  variant?: ToastProps["variant"];
  action?: ToastActionElement;
};

type ToastState = ToastOptions & {
  id: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

const TOAST_LIMIT = 3;
const TOAST_REMOVE_DELAY = 5000;

const listeners: Array<(state: ToastState[]) => void> = [];
let memoryState: ToastState[] = [];

function emitChange(state: ToastState[]) {
  listeners.forEach((listener) => listener(state));
}

function addToast(toast: ToastState) {
  memoryState = [toast, ...memoryState].slice(0, TOAST_LIMIT);
  emitChange(memoryState);

  setTimeout(() => {
    dismissToast(toast.id);
  }, TOAST_REMOVE_DELAY);
}

function dismissToast(id: string) {
  memoryState = memoryState.filter((toast) => toast.id !== id);
  emitChange(memoryState);
}

function useToast() {
  const [toasts, setToasts] = React.useState<ToastState[]>(memoryState);

  React.useEffect(() => {
    listeners.push(setToasts);
    return () => {
      const index = listeners.indexOf(setToasts);
      if (index > -1) {
        listeners.splice(index, 1);
      }
    };
  }, []);

  const toast = React.useCallback((options: ToastOptions) => {
    const id = crypto.randomUUID();
    addToast({
      id,
      open: true,
      onOpenChange: (open) => {
        if (!open) {
          dismissToast(id);
        }
      },
      ...options,
    });
  }, []);

  return { toast, toasts };
}

export { useToast };
export type { ToastState, ToastOptions, ToastActionElement, ToastProps };
