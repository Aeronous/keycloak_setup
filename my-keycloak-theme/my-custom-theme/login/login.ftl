<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=false displayWide=true; section>
<div class="login-container">

    <div class="left-panel"></div>

    <div class="right-panel">
        <div style="text-align: center;">
            <img class="logo" src="${url.resourcesPath}/img/logo.png" alt="Logo"/>
        </div>

        <div class="step-indicator">
            <div class="active">Identification</div>
            <div>Configurations</div>
        </div>

        <form id="kc-form-login" action="${url.loginAction}" method="post">
            <div class="form-field">
                <label for="username">User Name</label>
                <input type="text" id="username" name="username" value="${login.username!''}" required autofocus placeholder="Enter your user name" />
            </div>

            <div class="form-field">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" placeholder="Enter your password" required />
            </div>

            <input type="hidden" name="credentialId" value="${auth.selectedCredential?c}" />

            <button type="submit">Continue</button>

            <#if message?has_content>
                <div class="message ${message.type}">${message.summary}</div>
            </#if>
        </form>
    </div>

</div>
</@layout.registrationLayout>
