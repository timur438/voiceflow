import CryptoJS from 'crypto-js';

export const decryptTranscriptData = (encryptedData: string, key: string) => {
  const bytes = CryptoJS.AES.decrypt(encryptedData, key);
  return bytes.toString(CryptoJS.enc.Utf8);
};

export const getAccessToken = () => {
  return document.cookie.match(/access_token=([^;]+)/)?.[1] || null;
};

export const getDecryptedKey = () => {
  return document.cookie.match(/decrypted_key=([^;]+)/)?.[1] || null;
};