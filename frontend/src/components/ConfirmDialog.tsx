"use client";

type Props = {
  open: boolean;
  title: string;
  message: string;
  itemName?: string;
  confirmText?: string;
  cancelText?: string;
  onConfirm: () => void;
  onCancel: () => void;
};

export default function ConfirmDialog({
  open,
  title,
  message,
  itemName,
  confirmText = "Delete",
  cancelText = "Cancel",
  onConfirm,
  onCancel,
}: Props) {
  if (!open) return null;

  return (
    <div
      className="
        fixed
        inset-0
        bg-black/60
        flex
        items-center
        justify-center
        z-50
      "
    >
      <div
        className="
          w-[420px]
          bg-zinc-900
          border
          border-zinc-700
          rounded-xl
          shadow-2xl
          p-6
        "
      >
        <h2 className="text-xl font-semibold text-white">
          {title}
        </h2>

        <p className="mt-3 text-zinc-300">
          {message}
        </p>

        {itemName && (
          <p
            className="
              mt-2
              font-medium
              text-white
              break-all
            "
          >
            {itemName}
          </p>
        )}

        <p className="mt-4 text-sm text-zinc-500">
          This action cannot be undone.
        </p>

        <div className="flex justify-end gap-3 mt-6">

          <button
            onClick={onCancel}
            className="
              px-4
              py-2
              rounded-lg
              bg-zinc-700
              hover:bg-zinc-600
            "
          >
            {cancelText}
          </button>

          <button
            onClick={onConfirm}
            className="
              px-4
              py-2
              rounded-lg
              bg-red-600
              hover:bg-red-500
              transition
            "
          >
            {confirmText}
          </button>

        </div>
      </div>
    </div>
  );
}