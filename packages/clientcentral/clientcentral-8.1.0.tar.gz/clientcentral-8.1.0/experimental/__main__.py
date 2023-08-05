from clientcentral.clientcentral import ClientCentral

if __name__ == "__main__":
    cc = ClientCentral(production=False, token="m4nW9tIljQtoby2UpqUCF0QVJSHrYBsf")
    ticket = cc.get_ticket_by_id(86456)
    ticket.commit("test", commit_visisble_to_customer=True)
    # print(ticket.events)
    #for event in ticket.events:
    #    print(event.__dict__)