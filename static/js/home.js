
    	var home = document.getElementById('home');
    	var app = document.getElementById('app');
    	var os = document.getElementById('os');
    	var bm = document.getElementById('bm');
    	var au = document.getElementById('au');
    	var sign = document.getElementById('sign');
    	var login = document.getElementById('login');

    	home.style.color='red';

    	// app.style.color='red';

    	home.onclick=function ()
    	{
    		home.style.color='red';
    		app.style.color='white';
    		os.style.color='white';
    		bm.style.color='white';
    		au.style.color='white';
    		sign.style.color='white';
    		login.style.color='white';
    	}


    	app.onclick=function ()
    	{
    		home.style.color='white';
    		app.style.color='red';
    		os.style.color='white';
    		bm.style.color='white';
    		au.style.color='white';
    		sign.style.color='white';
    		login.style.color='white';
    	}

    	os.onclick=function ()
    	{
    		home.style.color='white';
    		app.style.color='white';
    		os.style.color='red';
    		bm.style.color='white';
    		au.style.color='white';
    		sign.style.color='white';
    		login.style.color='white';
    	}

    	bm.onclick=function ()
    	{
    		home.style.color='white';
    		app.style.color='white';
    		os.style.color='white';
    		bm.style.color='red';
    		au.style.color='white';
    		sign.style.color='white';
    		login.style.color='white';
    	}

    	au.onclick=function ()
    	{
    		home.style.color='white';
    		app.style.color='white';
    		os.style.color='white';
    		bm.style.color='white';
    		au.style.color='red';
    		sign.style.color='white';
    		login.style.color='white';
    	}

    	sign.onclick=function ()
    	{
    		home.style.color='white';
    		app.style.color='white';
    		os.style.color='white';
    		bm.style.color='white';
    		au.style.color='white';
    		sign.style.color='red';
    		login.style.color='white';
    	}

    	login.onclick=function ()
    	{
    		home.style.color='white';
    		app.style.color='white';
    		os.style.color='white';
    		bm.style.color='white';
    		au.style.color='white';
    		sign.style.color='white';
    		login.style.color='red';
    	}