post("/api/generate-password",{mode:"passphrase",words:4}).then(j=>$("ex").textContent=j.password);
