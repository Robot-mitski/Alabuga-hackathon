export class RegFormListener {
    #CommunicatorInstance;
    constructor(Instance){
        this.#CommunicatorInstance = Instance;
    }

    async OnSubmit(event){
        console.log(this);
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
        var resp = await this.#CommunicatorInstance.SendResponse("registration", {
            action: "registration",
            email: email,
            pass: pass
        }).then((json)=> {return json});
        console.log(resp);
        if (resp.status !== "ok") 
            return false;
        return true;
    }
}