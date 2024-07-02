export class RegFormListener {
    #CommunicatorInstance;
    constructor(Instance){
        this.#CommunicatorInstance = Instance;
    }

    async OnSubmit(event){
        event.preventDefault();
        var form = document.getElementById("regForm");
		var error = document.getElementById("regError");
		var email = form.regEmailField.value;
		var pass = form.regPassField.value;
        var rep_pass = form.regRepPassField.value;
        const EMAIL_RE = /^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/iu;
        if (email === "" || pass === "" || rep_pass === ""){
            error.innerHTML = "Заполните все поля";
            return false; }
        if (rep_pass !== pass) {
            error.innerHTML = "Пароли не совпадают";
            return false;}
        if (!EMAIL_RE.test(email)){
            error.innerHTML = "Неверный формат почтового адреса";
            return false; }
        var resp = await this.#CommunicatorInstance.SendResponse("registration", {
            "email": email,
            "pass": pass,
            "rep_pass": rep_pass
        }).then((json)=> {return json});
        var resp = JSON.parse(JSON.stringify(resp));
        if (resp.status !== "ok") {
            error.innerHTML = resp.message;
            return false;
        }
        window.location.href = "http://127.0.0.1:5000/user"
        return true;
    }
}