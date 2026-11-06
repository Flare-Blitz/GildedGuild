describe('Guest Login and start game', () => {
  it('should load the game page successfully', () => {
    cy.visit('http://localhost:3000/login')
    cy.get('#guest-login').click()
    cy.location('host').should('eq', 'localhost:3000');
    cy.get('#go-to-game').click();

    cy.url().should('include', '/game')
    cy.get('canvas').should('exist')
  })
})