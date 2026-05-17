import { useEffect, useMemo, useState } from "react";

import { Button } from "./components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import { Input } from "./components/ui/input";
import { useToast } from "./components/ui/use-toast";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

type DriveFile = {
  id: number;
  title: string;
  description: string;
  file_name: string;
  web_view_link: string;
  web_content_link?: string | null;
  uploaded_at: string;
};

const apiBaseUrl = API_BASE.replace(/\/$/, "");

export default function App() {
  const [driveFiles, setDriveFiles] = useState<DriveFile[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [editingFile, setEditingFile] = useState<DriveFile | null>(null);
  const [formTitle, setFormTitle] = useState("");
  const [formDescription, setFormDescription] = useState("");
  const [formFile, setFormFile] = useState<File | null>(null);
  const { toast } = useToast();

  const modalTitle = useMemo(
    () => (editingFile ? "Edit entry" : "Add entry"),
    [editingFile]
  );

  const loadFiles = async () => {
    setIsLoading(true);
    try {
      const response = await fetch(`${apiBaseUrl}/api/files/`);
      if (!response.ok) {
        throw new Error("Failed to fetch uploads.");
      }
      const data = (await response.json()) as DriveFile[];
      setDriveFiles(data);
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unable to load uploads.";
      toast({
        title: "Loading failed",
        description: message,
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    void loadFiles();
  }, []);

  const resetForm = () => {
    setFormTitle("");
    setFormDescription("");
    setFormFile(null);
  };

  const openCreateModal = () => {
    setEditingFile(null);
    resetForm();
    setIsModalOpen(true);
  };

  const openEditModal = (file: DriveFile) => {
    setEditingFile(file);
    setFormTitle(file.title || "");
    setFormDescription(file.description || "");
    setFormFile(null);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingFile(null);
    resetForm();
  };

  const handleSubmit = async () => {
    if (!formTitle.trim()) {
      toast({
        title: "Title required",
        description: "Add a title for this upload.",
        variant: "destructive",
      });
      return;
    }

    setIsSaving(true);
    try {
      const formData = new FormData();
      formData.append("title", formTitle.trim());
      formData.append("description", formDescription.trim());
      if (formFile) {
        formData.append("file", formFile);
      }

      const response = await fetch(
        editingFile
          ? `${apiBaseUrl}/api/files/${editingFile.id}/`
          : `${apiBaseUrl}/api/files/`,
        {
          method: editingFile ? "PATCH" : "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        throw new Error(errorPayload.detail || "Save failed.");
      }

      await loadFiles();
      const hasFile = Boolean(formFile || editingFile?.web_view_link);
      toast({
        title: editingFile ? "Entry updated" : "Entry saved",
        description: editingFile
          ? hasFile
            ? "Your changes are saved."
            : "Details saved without a file attached."
          : formFile
            ? "Your file is now available in Drive."
            : "Details saved without a file attached.",
      });
      closeModal();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unexpected save error.";
      toast({
        title: "Save failed",
        description: message,
        variant: "destructive",
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = async (file: DriveFile) => {
    const shouldDelete = window.confirm(
      `Delete "${file.title || file.file_name}"? Any linked Drive file will be removed.`
    );
    if (!shouldDelete) {
      return;
    }

    try {
      const response = await fetch(`${apiBaseUrl}/api/files/${file.id}/`, {
        method: "DELETE",
      });

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        throw new Error(errorPayload.detail || "Delete failed.");
      }

      setDriveFiles((prev) => prev.filter((item) => item.id !== file.id));
      toast({
        title: "Entry deleted",
        description: "The entry was removed and any linked file was deleted.",
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unexpected delete error.";
      toast({
        title: "Delete failed",
        description: message,
        variant: "destructive",
      });
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100">
      <div className="mx-auto flex w-full max-w-5xl flex-col gap-6">
        <Card className="border-slate-800 bg-slate-900/70">
          <CardHeader className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <CardTitle>Drive uploads</CardTitle>
              <CardDescription>
                Track uploads with titles, descriptions, and quick links.
              </CardDescription>
            </div>
            <Button onClick={openCreateModal}>Add entry</Button>
          </CardHeader>
          <CardContent>
            <div className="overflow-hidden rounded-lg border border-slate-800">
              <div className="grid grid-cols-12 gap-4 bg-slate-900/80 px-4 py-3 text-xs font-semibold uppercase text-slate-400">
                <div className="col-span-3">Title</div>
                <div className="col-span-3">Description</div>
                <div className="col-span-2">File URL</div>
                <div className="col-span-2">Date added</div>
                <div className="col-span-2 text-right">Actions</div>
              </div>
              <div className="divide-y divide-slate-800">
                {isLoading ? (
                  <div className="px-4 py-6 text-sm text-slate-400">
                    Loading uploads...
                  </div>
                ) : driveFiles.length === 0 ? (
                  <div className="px-4 py-6 text-sm text-slate-400">
                    No uploads yet. Add one to get started.
                  </div>
                ) : (
                  driveFiles.map((file) => (
                    <div
                      key={file.id}
                      className="grid grid-cols-12 gap-4 px-4 py-4 text-sm"
                    >
                      <div className="col-span-3 font-medium text-slate-100">
                        {file.title || file.file_name}
                      </div>
                      <div className="col-span-3 text-slate-300">
                        {file.description || "—"}
                      </div>
                      <div className="col-span-2">
                        {file.web_view_link ? (
                          <a
                            href={file.web_view_link}
                            target="_blank"
                            rel="noreferrer"
                            className="text-sky-400 underline"
                          >
                            View
                          </a>
                        ) : (
                          <span className="text-slate-500">No file</span>
                        )}
                      </div>
                      <div className="col-span-2 text-slate-300">
                        {new Date(file.uploaded_at).toLocaleString()}
                      </div>
                      <div className="col-span-2 flex items-center justify-end gap-2">
                        <Button
                          variant="outline"
                          onClick={() => openEditModal(file)}
                        >
                          Edit
                        </Button>
                        <Button
                          variant="destructive"
                          onClick={() => handleDelete(file)}
                        >
                          Delete
                        </Button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {isModalOpen ? (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 px-4">
          <div className="w-full max-w-lg rounded-2xl border border-slate-800 bg-slate-900 p-6 shadow-xl">
            <div className="mb-4 flex items-start justify-between gap-4">
              <div>
                <h2 className="text-lg font-semibold text-slate-100">
                  {modalTitle}
                </h2>
                <p className="text-sm text-slate-400">
                  {editingFile
                    ? "Update details or replace the file (optional)."
                    : "Add a title and description. File upload is optional."}
                </p>
              </div>
              <button
                type="button"
                className="text-slate-400 transition hover:text-slate-200"
                onClick={closeModal}
              >
                ✕
              </button>
            </div>
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase text-slate-400">
                  Title
                </label>
                <Input
                  value={formTitle}
                  onChange={(event) => setFormTitle(event.target.value)}
                  placeholder="Quarterly report"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase text-slate-400">
                  Description
                </label>
                <textarea
                  value={formDescription}
                  onChange={(event) => setFormDescription(event.target.value)}
                  placeholder="Short summary of this upload"
                  rows={4}
                  className="w-full rounded-md border border-slate-800 bg-slate-950 px-3 py-2 text-sm text-slate-100 outline-none focus:border-slate-600"
                />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-semibold uppercase text-slate-400">
                  File upload (optional)
                </label>
                <Input
                  type="file"
                  onChange={(event) =>
                    setFormFile(event.target.files?.[0] ?? null)
                  }
                />
                <p className="text-xs text-slate-400">
                  Leave empty to keep the current file or save without one.
                </p>
              </div>
            </div>
            <div className="mt-6 flex items-center justify-end gap-3">
              <Button variant="outline" onClick={closeModal}>
                Cancel
              </Button>
              <Button onClick={handleSubmit} disabled={isSaving}>
                {isSaving ? "Saving..." : "Save entry"}
              </Button>
            </div>
          </div>
        </div>
      ) : null}
    </main>
  );
}
