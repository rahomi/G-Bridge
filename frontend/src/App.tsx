import { useState } from "react";

import { Button } from "./components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "./components/ui/card";
import { Input } from "./components/ui/input";
import { useToast } from "./components/ui/use-toast";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [webViewLink, setWebViewLink] = useState<string | null>(null);
  const { toast } = useToast();

  const handleUpload = async () => {
    if (!selectedFile) {
      toast({
        title: "Select a file",
        description: "Choose a file before uploading to Drive.",
        variant: "destructive",
      });
      return;
    }

    setIsUploading(true);
    setWebViewLink(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(
        `${API_BASE.replace(/\/$/, "")}/api/upload/`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorPayload = await response.json().catch(() => ({}));
        throw new Error(errorPayload.detail || "Upload failed.");
      }

      const data = await response.json();
      setWebViewLink(data.web_view_link);

      toast({
        title: "Upload complete",
        description: "Your file is now available in Google Drive.",
      });
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Unexpected upload error.";
      toast({
        title: "Upload failed",
        description: message,
        variant: "destructive",
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <main className="min-h-screen bg-slate-950 px-6 py-12 text-slate-100">
      <div className="mx-auto flex w-full max-w-2xl flex-col gap-6">
        <Card className="border-slate-800 bg-slate-900/70">
          <CardHeader>
            <CardTitle>Google Drive uploader</CardTitle>
            <CardDescription>
              Upload a file and get the shareable Drive link instantly.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <Input
              type="file"
              onChange={(event) =>
                setSelectedFile(event.target.files?.[0] ?? null)
              }
            />
            <p className="text-sm text-slate-400">
              Files are uploaded to the configured Drive folder using the API.
            </p>
          </CardContent>
          <CardFooter className="flex items-center justify-between gap-4">
            <Button onClick={handleUpload} disabled={isUploading}>
              {isUploading ? "Uploading..." : "Upload to Drive"}
            </Button>
            {webViewLink ? (
              <a
                href={webViewLink}
                target="_blank"
                rel="noreferrer"
                className="text-sm text-sky-400 underline"
              >
                View file
              </a>
            ) : (
              <span className="text-sm text-slate-500">No upload yet</span>
            )}
          </CardFooter>
        </Card>
      </div>
    </main>
  );
}
