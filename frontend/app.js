import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function ResumeGenerator() {
  const [jobDescription, setJobDescription] = useState("");
  const [additionalInfo, setAdditionalInfo] = useState("");
  const [generatedText, setGeneratedText] = useState("");
  const [modificationPrompt, setModificationPrompt] = useState("");

  const handleGenerate = async (type) => {
    // Placeholder for AI API call
    setGeneratedText(`${type} generated for: \n${jobDescription}`);
  };

  const handleModify = async () => {
    // Placeholder for AI API call
    setGeneratedText(`Modified: ${modificationPrompt}\n${generatedText}`);
  };

  return (
    <div className="grid grid-cols-3 gap-4 p-4">
      <Card className="col-span-1 p-4">
        <h2 className="text-lg font-bold">Additional Information</h2>
        <Textarea
          value={additionalInfo}
          onChange={(e) => setAdditionalInfo(e.target.value)}
          placeholder="Enter any additional details..."
          className="mt-2"
        />
      </Card>

      <Card className="col-span-2 p-4">
        <h2 className="text-lg font-bold">Job Description</h2>
        <Textarea
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          placeholder="Paste the job description here..."
          className="mt-2"
        />
        <div className="flex gap-2 mt-4">
          <Button onClick={() => handleGenerate("Resume")}>Generate Resume</Button>
          <Button onClick={() => handleGenerate("Cover Letter")}>Generate Cover Letter</Button>
        </div>

        {generatedText && (
          <Card className="mt-4 p-4">
            <h3 className="text-lg font-bold">Generated Content</h3>
            <p className="mt-2 whitespace-pre-wrap">{generatedText}</p>
            <Textarea
              value={modificationPrompt}
              onChange={(e) => setModificationPrompt(e.target.value)}
              placeholder="Modify the content..."
              className="mt-2"
            />
            <Button onClick={handleModify} className="mt-2">Apply Modifications</Button>
          </Card>
        )}
      </Card>
    </div>
  );
}
