<#import "template.ftl" as layout>
<@layout.registrationLayout displayInfo=false displayWide=true; section>
    <#if section = "header">
        <!-- Custom header if needed -->
    <#elseif section = "form">
        <div class="login-container">
            <!-- Left side - Logo and background -->
            <div class="login-container__left">
                <img src="${url.resourcesPath}/images/logo.svg" alt="Aeronous Solutions" class="login-container__logo" />
            </div>

            <!-- Right side - Login form -->
            <div class="login-container__right">
                <div class="login-container__container">
                    <!-- Step indicators -->
                    <div class="login-container__steps">
                        <div class="stepper">
                            <div class="step">
                                <div class="circle active"></div>
                                <div class="label">Identification</div>
                            </div>
                            <div class="line"></div>
                            <div class="step">
                                <div class="circle"></div>
                                <div class="label">Configurations</div>
                            </div>
                        </div>
                    </div>

                    <!-- Login Form -->
                    <form id="kc-form-login" class="login-container__form" action="${url.loginAction}" method="post">
                        <div class="login-container__field">
                            <label for="username" class="login-container__label">
                                <#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>
                            </label>
                            <input tabindex="1" id="username" class="login-container__input" name="username" value="${(login.username!'')}"
                                   type="text" autofocus autocomplete="off"
                                   aria-invalid="<#if message?has_content && message.type = 'error'>true</#if>"
                                   placeholder="<#if !realm.loginWithEmailAllowed>${msg("username")}<#elseif !realm.registrationEmailAsUsername>${msg("usernameOrEmail")}<#else>${msg("email")}</#if>" />
                        </div>

                        <div class="login-container__field">
                            <label for="password" class="login-container__label">${msg("password")}</label>
                            <input tabindex="2" id="password" class="login-container__input" name="password" type="password" autocomplete="off"
                                   aria-invalid="<#if message?has_content && message.type = 'error'>true</#if>"
                                   placeholder="${msg("password")}" />
                        </div>

                        <#if realm.rememberMe && !usernameEditDisabled??>
                            <div class="login-container__checkbox">
                                <label>
                                    <#if login.rememberMe??>
                                        <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox" checked> ${msg("rememberMe")}
                                    <#else>
                                        <input tabindex="3" id="rememberMe" name="rememberMe" type="checkbox"> ${msg("rememberMe")}
                                    </#if>
                                </label>
                            </div>
                        </#if>

                        <#if message?has_content && (message.type != 'warning' || !isAppInitiatedAction??)>
                            <div class="login-container__error">
                                ${kcSanitize(message.summary)?no_esc}
                            </div>
                        </#if>

                        <div class="login-container__button-container">
                            <button tabindex="4" class="login-container__button" name="login" id="kc-login" type="submit">
                                Enter
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </#if>
</@layout.registrationLayout>
