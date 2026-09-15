/** ONNX embedding models that require local model downloads. GenAI providers are not in this list. */
export const JINA_EMBEDDING_MODELS = ["jinav1", "jinav2"] as const;

/**
 * Sentinel the backend substitutes for saved credentials (api keys,
 * passwords, secrets) in /config responses. The credential widget renders
 * this value as an empty input with a "saved — leave blank to keep" hint,
 * and stripRedactedCredentials() removes any field still equal to this
 * value before sending a config/set payload so the saved YAML value is
 * preserved.
 */
export const REDACTED_CREDENTIAL_SENTINEL = "__ARCVISION_SAVED_CREDENTIAL__";
export const LEGACY_REDACTED_CREDENTIAL_SENTINEL = "__FRIGATE_SAVED_CREDENTIAL__";

export const isRedactedCredential = (value: unknown): boolean =>
  value === REDACTED_CREDENTIAL_SENTINEL ||
  value === LEGACY_REDACTED_CREDENTIAL_SENTINEL;

export const ANNOTATION_OFFSET_MIN = -10000;
export const ANNOTATION_OFFSET_MAX = 10000;
export const ANNOTATION_OFFSET_STEP = 50;

export const supportedLanguageKeys = ["en", "hi", "gu"];
