import CryptoJS from "crypto-js";

export const decryptTranscriptData = (encryptedData: string, key: string) => {
  const bytes = CryptoJS.enc.Base64.parse(encryptedData);

  const iv = CryptoJS.enc.Base64.stringify(bytes.clone().words.slice(0, 4));

  const ciphertext = bytes.clone().words.slice(4);

  const decryptedBytes = CryptoJS.AES.decrypt(
    { ciphertext: CryptoJS.lib.CipherParams.create({ ciphertext }) },
    CryptoJS.enc.Utf8.parse(key),
    { iv: CryptoJS.enc.Base64.parse(iv) },
  );

  return decryptedBytes.toString(CryptoJS.enc.Utf8);
};

export const getAccessToken = () => {
  return document.cookie.match(/access_token=([^;]+)/)?.[1] || null;
};

export const getDecryptedKey = () => {
  return document.cookie.match(/decrypted_key=([^;]+)/)?.[1] || null;
};
