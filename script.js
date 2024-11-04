
// PARTE 1

document.getElementById('btnCifrar').addEventListener('click', function() {
    const texto = document.getElementById('inputTexto').value;
    const chave = document.getElementById('inputChave').value;
    const semAcentos = removeAcentos(texto);
    const textoCifrado = vigenereEncrypt(semAcentos, chave);
    document.getElementById('outputTexto').value = textoCifrado;
});

document.getElementById('btnDecifrar').addEventListener('click', function() {
    const texto = document.getElementById('inputTexto').value;
    const chave = document.getElementById('inputChave').value;
    const textoDecifrado = vigenereDecrypt(texto, chave);
    document.getElementById('outputTexto').value = textoDecifrado;
});

// PARTE 2

document.getElementById('btnDescobrirChave').addEventListener('click', function() {
    const textoCifrado = document.getElementById('inputTextoCifrado').value;
    const idioma = document.getElementById('inputIdioma').value;
    const cleanText = prepareCiphertext(textoCifrado);
    const keyLength = estimateKeyLength(cleanText, idioma);
    const initialKey = findKey(cleanText, keyLength, idioma);
    const chaveDescoberta = findRepetitivePattern(initialKey);
    const textoDecifrado = decryptWithKey(textoCifrado, chaveDescoberta);
    document.getElementById('outputTextoDecifrado').value = textoDecifrado;
    document.getElementById('outputChave').value = chaveDescoberta;

});

document.getElementById('clearButton1').addEventListener('click', clearText1);
document.getElementById('clearButton2').addEventListener('click', clearText2);

function clearText1() {
  document.getElementById('inputTexto').value = '';
  document.getElementById('outputTexto').value = '';
  document.getElementById('inputChave').value = '';
}

function clearText2() {
  document.getElementById('inputTextoCifrado').value = '';
  document.getElementById('outputTextoDecifrado').value = '';
  document.getElementById('outputChave').value = '';
}

// Função para remover acentos de uma string
function removeAcentos(texto) {
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

// Função para criptografar usando a cifra de Vigenère
function vigenereEncrypt(plaintext, key) {
    plaintext = plaintext.toUpperCase(); // Remove acentos e transforma em maiúsculas
    key = key.toUpperCase();

    let ciphertext = [];
    let keyLength = key.length;
    let keyIndex = 0;

    for (let char of plaintext) {
        if (/[A-Z]/.test(char)) { // Verifica se o caractere é uma letra
            let shift = key.charCodeAt(keyIndex % keyLength) - "A".charCodeAt(0);
            let encryptedChar = String.fromCharCode(((char.charCodeAt(0) - "A".charCodeAt(0) + shift) % 26) + "A".charCodeAt(0));
            ciphertext.push(encryptedChar);
            keyIndex++;
        } else {
            ciphertext.push(char); // Mantém caracteres não alfabéticos inalterados
        }
    }

    return ciphertext.join("").toLowerCase(); // Converte o texto criptografado para minúsculas
}

// Função para descriptografar usando a cifra de Vigenère
function vigenereDecrypt(ciphertext, key) {
    ciphertext = ciphertext.toUpperCase();
    key = key.toUpperCase();

    let plaintext = [];
    let keyLength = key.length;
    let keyIndex = 0;

    for (let char of ciphertext) {
        if (/[A-Z]/.test(char)) { // Verifica se o caractere é uma letra
            let shift = key.charCodeAt(keyIndex % keyLength) - "A".charCodeAt(0);
            let decryptedChar = String.fromCharCode(((char.charCodeAt(0) - "A".charCodeAt(0) - shift + 26) % 26) + "A".charCodeAt(0));
            plaintext.push(decryptedChar);
            keyIndex++;
        } else {
            plaintext.push(char); // Mantém caracteres não alfabéticos inalterados
        }
    }

    return plaintext.join("").toLowerCase(); // Converte o texto descriptografado para minúsculas
}


// PARTE 2 A PARTIR DAQUI
















const englishFrequencies = {
    'A': 8.167, 'B': 1.492, 'C': 2.782, 'D': 4.253, 'E': 12.702,
    'F': 2.228, 'G': 2.015, 'H': 6.094, 'I': 6.966, 'J': 0.153,
    'K': 0.772, 'L': 4.025, 'M': 2.406, 'N': 6.749, 'O': 7.507,
    'P': 1.929, 'Q': 0.095, 'R': 5.987, 'S': 6.327, 'T': 9.056,
    'U': 2.758, 'V': 0.978, 'W': 2.360, 'X': 0.150, 'Y': 1.974,
    'Z': 0.074
}

const portugueseFrequencies = {
    'A': 14.63, 'B': 1.04, 'C': 3.88, 'D': 4.99, 'E': 12.57,
    'F': 1.02, 'G': 1.30, 'H': 1.28, 'I': 6.18, 'J': 0.40,
    'K': 0.02, 'L': 2.78, 'M': 4.74, 'N': 5.05, 'O': 10.73,
    'P': 2.52, 'Q': 1.20, 'R': 6.53, 'S': 7.81, 'T': 4.34,
    'U': 4.63, 'V': 1.67, 'W': 0.01, 'X': 0.21, 'Y': 0.01,
    'Z': 0.47
  };
  
  function prepareCiphertext(text) {
    return text.toUpperCase().replace(/[^A-Z]/g, '');
  }
  
  function calculateIndexOfCoincidence(text) {
    const n = text.length;
    const frequencies = [...text].reduce((freq, char) => {
      freq[char] = (freq[char] || 0) + 1;
      return freq;
    }, {});
    
    const ic = n > 1
      ? Object.values(frequencies).reduce((sum, f) => sum + f * (f - 1), 0) / (n * (n - 1))
      : 0;
  
    return ic;
  }
  
  function estimateKeyLength(ciphertext, language, maxKeyLength = 20) {
    let ic_chosen = 0.068;
    const ic_portuguese = 0.072;
    const ic_english = 0.068;
    
    if (language == "portuguese") {
      ic_chosen = ic_portuguese;
    }
    else {
      ic_chosen = ic_english;
    }

    let bestKeyLength = 1;
    let minDiff = Infinity;
  
    for (let keyLength = 1; keyLength <= maxKeyLength; keyLength++) {
      let icSum = 0;
      
      for (let i = 0; i < keyLength; i++) {
        const group = [...ciphertext].filter((_, index) => index % keyLength === i).join('');
        icSum += calculateIndexOfCoincidence(group);
      }
  
      const icAvg = icSum / keyLength;
      const diff = Math.abs(icAvg - ic_chosen);
  
      if (diff < minDiff) {
        minDiff = diff;
        bestKeyLength = keyLength;
      }
    }
  
    return bestKeyLength;
  }
  
  function chiSquaredStat(observed, expected) {
    return Object.keys(expected).reduce((sum, letter) => {
      const observedFreq = observed[letter] || 0;
      return sum + Math.pow(observedFreq - expected[letter], 2) / expected[letter];
    }, 0);
  }
  
  function calculateLetterFrequencies(text) {
    const n = text.length;
    const freq = [...text].reduce((acc, char) => {
      acc[char] = (acc[char] || 0) + 1;
      return acc;
    }, {});
  
    return Object.fromEntries(
      Object.entries(freq).map(([letter, count]) => [letter, (count / n) * 100])
    );
  }
  
  function decryptWithKey(ciphertext, key) {
    const keyLength = key.length;
    let keyIndex = 0;
  
    return [...ciphertext].map(char => {
      if (/[A-Z]/.test(char)) {
        const shift = key[keyIndex % keyLength].charCodeAt(0) - 'A'.charCodeAt(0);
        const decryptedChar = String.fromCharCode((char.charCodeAt(0) - shift - 'A'.charCodeAt(0) + 26) % 26 + 'A'.charCodeAt(0));
        keyIndex++;
        return decryptedChar;
      } else if (/[a-z]/.test(char)) {
        const shift = key[keyIndex % keyLength].charCodeAt(0) - 'A'.charCodeAt(0);
        const decryptedChar = String.fromCharCode((char.toUpperCase().charCodeAt(0) - shift - 'A'.charCodeAt(0) + 26) % 26 + 'A'.charCodeAt(0)).toLowerCase();
        keyIndex++;
        return decryptedChar;
      } else {
        return char;
      }
    }).join('');
  }
  
  function findKey(ciphertext, keyLength, language) {
    let key = [];
  
    for (let i = 0; i < keyLength; i++) {
      const group = [...ciphertext].filter((_, index) => index % keyLength === i).join('');
      const observedFreq = calculateLetterFrequencies(group);
      let minChiSquared = Infinity;
      let bestShift = null;
  
      for (let shift = 0; shift < 26; shift++) {
        const shiftedFreq = Object.fromEntries(
          Object.entries(observedFreq).map(([letter, freq]) => [
            String.fromCharCode((letter.charCodeAt(0) - shift - 'A'.charCodeAt(0) + 26) % 26 + 'A'.charCodeAt(0)),
            freq
          ])
        );
        const chiSquared = chiSquaredStat(shiftedFreq, language == "portuguese" ? portugueseFrequencies : englishFrequencies);
        console.log(language);

        if (chiSquared < minChiSquared) {
          minChiSquared = chiSquared;
          bestShift = shift;
        }
      }
  
      key.push(String.fromCharCode('A'.charCodeAt(0) + bestShift));
    }
  
    return key.join('');
  }
  
  function findRepetitivePattern(key) {
    for (let i = 1; i <= key.length / 2; i++) {
      const pattern = key.slice(0, i);
      if (pattern.repeat(key.length / pattern.length) === key) {
        return pattern;
      }
    }
    return key;
  }