export type Lead = {
  id: number;
  name: string;
  phone?: string | null;
  budget?: string | null;
  location?: string | null;
  property_type?: string | null;
  bhk?: string | null;
  intent?: string | null;
  notes?: string | null;
  transcript?: string | null;
  language?: string | null;
  source?: string | null;
  status: string;
  priority?: string | null;
  summary?: string | null;
  next_action?: string | null;
  request_id?: string | null;
  created_at?: string;
  updated_at?: string;
};

export type Health = {
  status: string;
  service: string;
  version: string;
  environment: string;
  gnani_configured: boolean;
  stt_model: string;
  tts_model: string;
};

export type TranscriptResponse = {
  transcript: string;
  language: string;
  request_id?: string | null;
  extracted?: Record<string, string | null>;
};