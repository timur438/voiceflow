import CryptoJS from "crypto-js";

export const decryptTranscriptData = (encryptedData: string, key: string) => {
  try {
    const parsedData = CryptoJS.enc.Base64.parse(encryptedData);
    
    const iv = CryptoJS.lib.WordArray.create(parsedData.words.slice(0, 4));
    
    const ciphertext = CryptoJS.lib.WordArray.create(parsedData.words.slice(4));
    
    const decrypted = CryptoJS.AES.decrypt(
      { ciphertext: ciphertext } as CryptoJS.lib.CipherParams,
      CryptoJS.enc.Utf8.parse(key),
      { iv: iv }
    );
    
    return decrypted.toString(CryptoJS.enc.Utf8);
  } catch (error) {
    console.error("Decryption error:", error);
    return null;
  }
};

export const getAccessToken = () => {
  return document.cookie.match(/access_token=([^;]+)/)?.[1] || null;
};

export const getDecryptedKey = () => {
  return document.cookie.match(/decrypted_key=([^;]+)/)?.[1] || null;
};
