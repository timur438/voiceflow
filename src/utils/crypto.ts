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

export const decryptTranscriptData = (
  encryptedData: string,
  key: string
): Meeting | null => {
  try {
    if (!encryptedData?.trim() || !key?.trim()) {
      console.error("Invalid input parameters");
      return null;
    }

    const encryptedBytes = CryptoJS.enc.Base64.parse(encryptedData);
    console.debug("Encrypted bytes:", encryptedBytes);

    if (encryptedBytes.sigBytes < 32) {
      console.error("Data too short for decryption");
      return null;
    }

    const iv = CryptoJS.lib.WordArray.create(
      encryptedBytes.words.slice(0, 4),
      16 // 16 bytes
    );
    console.debug("IV:", iv.toString());

    const ciphertext = CryptoJS.lib.WordArray.create(
      encryptedBytes.words.slice(4),
      encryptedBytes.sigBytes - 16
    );
    console.debug("Ciphertext length:", ciphertext.sigBytes);

    const cfg = {
      iv: iv,
      mode: CryptoJS.mode.CBC,
      padding: CryptoJS.pad.Pkcs7
    };

    const decrypted = CryptoJS.AES.decrypt(
      { ciphertext: ciphertext } as CryptoJS.lib.CipherParams,
      CryptoJS.enc.Utf8.parse(key),
      cfg
    );

    const rawString = decrypted.toString(CryptoJS.enc.Latin1);
    console.debug("Raw decrypted:", rawString);

    try {
      const result = JSON.parse(rawString);
      
      if (!result?.id || typeof result.name !== "string") {
        console.error("Invalid decrypted structure");
        return null;
      }

      return {
        id: result.id,
        date: result.date || new Date().toISOString().split('T')[0],
        name: result.name,
        status: result.status === "old" ? "old" : "new",
        length: result.length || "00:00"
      };
    } catch (e) {
      console.error("JSON parse failed:", e);
      return null;
    }
  } catch (error) {
    console.error("Full decryption error:", error);
    return null;
  }
};

export const getAccessToken = () => {
  return document.cookie.match(/access_token=([^;]+)/)?.[1] || null;
};

export const getDecryptedKey = () => {
  return document.cookie.match(/decrypted_key=([^;]+)/)?.[1] || null;
};
