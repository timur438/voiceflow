import CryptoJS from "crypto-js";

interface Meeting {
  id: number;
  date: string;
  name: string;
  status: "new" | "old";
  length: string;
  transcript?: string;
  speakers?: string[];
}


export const decryptTranscriptData = (encryptedData: string, key: string): Meeting | null => {
  try {
    if (!encryptedData || !key) {
      console.error("Missing encrypted data or key");
      return null;
    }

    const encryptedBytes = CryptoJS.enc.Base64.parse(encryptedData);
    
    if (encryptedBytes.words.length < 4) {
      console.error("Invalid encrypted data format");
      return null;
    }

    const iv = CryptoJS.lib.WordArray.create(encryptedBytes.words.slice(0, 4));
    
    const ciphertext = CryptoJS.lib.WordArray.create(encryptedBytes.words.slice(4));
    
    const decrypted = CryptoJS.AES.decrypt(
      { ciphertext } as CryptoJS.lib.CipherParams,
      CryptoJS.enc.Utf8.parse(key),
      { iv }
    );

    const decryptedString = decrypted.toString(CryptoJS.enc.Utf8);
    
    try {
      const result = JSON.parse(decryptedString);
      
      if (!result.id || !result.name) {
        console.error("Decrypted data has invalid format");
        return null;
      }
      
      return {
        id: result.id,
        date: result.date || new Date().toISOString(),
        name: result.name,
        status: result.status || "new",
        length: result.length || "00:00"
      };
    } catch (e) {
      console.error("JSON parse error:", e);
      return null;
    }
  } catch (error) {
    console.error("Decryption failed:", error);
    return null;
  }
};

export const getAccessToken = () => {
  return document.cookie.match(/access_token=([^;]+)/)?.[1] || null;
};

export const getDecryptedKey = () => {
  return document.cookie.match(/decrypted_key=([^;]+)/)?.[1] || null;
};
