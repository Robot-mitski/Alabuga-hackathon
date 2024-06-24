export class RegFormListener {
    #CommunicatorInstance;
    constructor(CommunicatorInstance){
        this.#CommunicatorInstance = CommunicatorInstance;
    }

    OnSubmit(){
        event.preventDefault();
        var form = document.getElementById("regForm");
		var error = document.getElementById("regError");
		var email = form.regEmailField.value;
		var pass = form.regPassField.value;
        const EMAIL_RE = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;
        if (email === "" || pass === ""){
            error.innerHTML = "Заполните все поля";
            return false; }
        if (!EMAIL_RE.test(email)){
            error.innerHTML = "Неверный формат почтового адреса";
            return false; }
        this.#CommunicatorInstance.SendResponse("", {
            action: "registration",
            email: email,
            pass: pass
        })
        return true;
    }
}